from django.shortcuts import render, redirect
from django.http import Http404
from django.views.generic import TemplateView, UpdateView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.conf import settings
import requests
from .models import Mandato, User, Planejamento, Objetivo, ArquivoBiblioteca
from .forms import MandatoForm, PlanejamentoForm


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
    """
    View para gestão de equipe
    """
    return render(request, 'core/equipe.html', {})


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


def sugestao_emendas(request, arquivo_id):
    """Gera sugestões de emendas a partir de um PDF"""
    if not request.user.is_authenticated:
        return redirect('account_login')

    user = request.user
    if not user.mandato:
        messages.error(request, 'Você precisa cadastrar seu mandato para usar esta função.')
        return redirect('core:meu_mandato')

    arquivo = get_object_or_404(ArquivoBiblioteca, id=arquivo_id, mandato=user.mandato)

    dados = {
        'nome_parlamentar': user.mandato.nome_parlamentar,
        'casa_legislativa': user.mandato.get_casa_legislativa_display(),
        'esfera': {
            Mandato.CasaLegislativa.CM: 'Municipal',
            Mandato.CasaLegislativa.ALE: 'Estadual',
            Mandato.CasaLegislativa.CF: 'Federal',
            Mandato.CasaLegislativa.SENADO: 'Federal',
        }.get(user.mandato.casa_legislativa, ''),
        'municipio': user.mandato.municipio,
        'ue': user.mandato.estado,
        'temas_interesse': getattr(getattr(user.mandato, 'planejamento', None), 'temas_interesse', ''),
        'perfil_parlamentar': user.mandato.get_perfil_display(),
        'espectro_politico': user.mandato.get_posicionamento_display(),
        'origem_legislativa': 'Legislativo',
    }

    sugestoes = None
    try:
        with arquivo.arquivo.open('rb') as f:
            files = {'file': f}
            headers = {'X-API-Key': settings.AI_API_KEY}
            url = f"{settings.AI_API_BASE_URL}/expert/pl/sugestao_emendas"
            resp = requests.post(url, headers=headers, files=files, data=dados, timeout=60)
            if resp.ok:
                sugestoes = resp.json()
            else:
                sugestoes = {'erro': f'Erro {resp.status_code} ao consultar API'}
    except Exception as exc:
        sugestoes = {'erro': str(exc)}

    return render(request, 'core/sugestao_emendas.html', {'arquivo': arquivo, 'sugestoes': sugestoes})
