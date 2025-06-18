from django.shortcuts import render, redirect
from django.http import Http404
from django.views.generic import TemplateView, UpdateView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from .models import Mandato, User, Planejamento, Objetivo, Invitation, AISettings, ArquivoBiblioteca
from .forms import MandatoForm, PlanejamentoForm, TeamMemberForm, AIConfigForm
from . import ai
from django.shortcuts import get_object_or_404
from django.conf import settings
import requests


class WelcomeView(LoginRequiredMixin, TemplateView):
    template_name = "core/welcome.html"
    login_url = reverse_lazy('account_login')


class MeuMandatoView(LoginRequiredMixin, UpdateView):
    model = Mandato
    form_class = MandatoForm
    template_name = "core/meu_mandato_form.html"
    success_url = reverse_lazy('core:welcome')
    login_url = reverse_lazy('account_login')

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if not request.user.is_authenticated or not isinstance(user, User):
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        user = self.request.user
        if isinstance(user, User):
            # If user has a mandate, return it for editing
            if user.mandato is not None:
                return user.mandato
            # If user doesn't have a mandate, create a new one
            else:
                return Mandato()
        raise Http404("Usuário não encontrado")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if isinstance(user, User) and user.mandato is None:
            context['is_creating'] = True
        else:
            context['is_creating'] = False
        return context

    def form_valid(self, form):
        user = self.request.user
        if isinstance(user, User):
            # Check if we're creating or updating
            if user.mandato is None:
                # Creating new mandate
                self.object = form.save()
                user.mandato = self.object
                user.save()
            else:
                # Updating existing mandate
                self.object = form.save()
        return super().form_valid(form)


def custom_404(request, exception):
    return render(request, '404.html', {}, status=404)

def planejamento_wizard(request):
    """
    View para o wizard de planejamento
    """
    return render(request, 'core/planejamento.html', {})

def gestao_equipe(request):
    """Página principal de gestão de equipe."""
    user = request.user
    if not user.is_authenticated or not user.mandato:
        return redirect('core:welcome')

    membros = user.mandato.usuarios.all()
    form = TeamMemberForm()
    return render(request, 'core/equipe.html', {
        'membros': membros,
        'form': form,
    })


@require_POST
def invite_member(request):
    form = TeamMemberForm(request.POST)
    if form.is_valid() and request.user.mandato:
        token = get_random_string(32)
        Invitation.objects.create(
            mandato=request.user.mandato,
            nome=form.cleaned_data['nome'],
            email=form.cleaned_data['email'],
            funcao=form.cleaned_data['funcao'],
            token=token,
        )
        signup_url = request.build_absolute_uri(reverse_lazy('account_signup'))
        send_mail(
            'Convite para integrar equipe',
            f'Você foi convidado para fazer parte da equipe. Cadastre-se em {signup_url} usando este email.',
            None,
            [form.cleaned_data['email']],
            fail_silently=True,
        )
        if request.headers.get('HX-Request'):
            membros = request.user.mandato.usuarios.all()
            return render(request, 'core/partials/member_list.html', {'membros': membros})
        return JsonResponse({'ok': True})
    return JsonResponse({'ok': False}, status=400)


@require_POST
def remove_member(request, user_id):
    if not request.user.mandato:
        return JsonResponse({'ok': False}, status=400)
    try:
        member = User.objects.get(pk=user_id, mandato=request.user.mandato)
        member.delete()
        if request.headers.get('HX-Request'):
            return HttpResponse('')
        return JsonResponse({'ok': True})
    except User.DoesNotExist:
        if request.headers.get('HX-Request'):
            return HttpResponse(status=404)
        return JsonResponse({'ok': False}, status=404)


@require_POST
def ai_suggestions(request):
    tipo = request.POST.get('tipo')
    mandato = request.user.mandato
    if tipo == 'cargos':
        num = int(request.POST.get('quantidade', '1'))
        sugestao = ai.suggest_positions(num, mandato)
    else:
        cargo = request.POST.get('cargo')
        sugestao = ai.suggest_tasks(cargo, mandato)
    return JsonResponse({'sugestao': sugestao})


def config_ai(request):
    settings = AISettings.get_solo()
    if request.method == 'POST':
        form = AIConfigForm(request.POST, instance=settings)
        if form.is_valid():
            form.save()
            messages.success(request, 'Configurações salvas com sucesso.')
            return redirect('core:config_ai')
    else:
        form = AIConfigForm(instance=settings)
    return render(request, 'core/config_ai.html', {'form': form})


class MeuPlanejamentoView(LoginRequiredMixin, UpdateView):
    model = Planejamento
    form_class = PlanejamentoForm
    template_name = "core/meu_planejamento_form.html"
    success_url = reverse_lazy('core:meu_planejamento')
    login_url = reverse_lazy('account_login')

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if not request.user.is_authenticated or not isinstance(user, User):
            return self.handle_no_permission()
        
        # Verificar se o usuário tem um mandato
        if not user.mandato:
            messages.warning(request, 'Você precisa criar seu mandato antes de fazer o planejamento.')
            return redirect('core:meu_mandato')
        
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        user = self.request.user
        if isinstance(user, User) and user.mandato:
            # Se o mandato tem planejamento, retorna para edição
            try:
                if hasattr(user.mandato, 'planejamento') and user.mandato.planejamento.pk:
                    return user.mandato.planejamento
            except Planejamento.DoesNotExist:
                pass
            
            # Se não tem planejamento, cria um novo
            return Planejamento(mandato=user.mandato)
        raise Http404("Planejamento não encontrado")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        if isinstance(user, User) and user.mandato:
            context['mandato'] = user.mandato
            # Verificar se está criando ou editando
            if hasattr(user.mandato, 'planejamento') and user.mandato.planejamento.pk:
                context['is_creating'] = False
                context['objetivos'] = user.mandato.planejamento.objetivos.all()
            else:
                context['is_creating'] = True
                context['objetivos'] = []
        
        return context

    def form_valid(self, form):
        user = self.request.user
        if isinstance(user, User) and user.mandato:
            # Se não tem planejamento ainda, associa ao mandato
            if not hasattr(user.mandato, 'planejamento'):
                form.instance.mandato = user.mandato
                messages.success(self.request, 'Planejamento criado com sucesso!')
            else:
                messages.success(self.request, 'Planejamento atualizado com sucesso!')

            self.object = form.save()
        return super().form_valid(form)