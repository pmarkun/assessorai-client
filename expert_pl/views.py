from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
import requests

from core.models import ArquivoBiblioteca
from .forms import ArquivoBibliotecaForm

@login_required
def sugestao_emendas(request):
    user = request.user
    if not user.mandato:
        messages.error(request, 'Você precisa cadastrar seu mandato para usar esta função.')
        return redirect('core:meu_mandato')

    arquivos = ArquivoBiblioteca.objects.filter(mandato=user.mandato).order_by('-created_at')
    form = ArquivoBibliotecaForm()
    sugestoes = None

    if request.method == 'POST':
        if 'delete_id' in request.POST:
            arquivo = get_object_or_404(ArquivoBiblioteca, id=request.POST['delete_id'], mandato=user.mandato)
            arquivo.delete()
            messages.success(request, 'Arquivo removido com sucesso.')
            return redirect('expert_pl:sugestao_emendas')

        if 'upload' in request.POST:
            form = ArquivoBibliotecaForm(request.POST, request.FILES)
            if form.is_valid():
                arquivo = form.save(commit=False)
                arquivo.mandato = user.mandato
                arquivo.save()
                messages.success(request, 'Arquivo enviado com sucesso.')
            else:
                messages.error(request, 'Erro ao enviar arquivo.')
            return redirect('expert_pl:sugestao_emendas')

        if 'generate' in request.POST:
            arquivo_id = request.POST.get('arquivo_id')
            if not arquivo_id:
                messages.error(request, 'Selecione um arquivo para gerar as sugestões.')
                return redirect('expert_pl:sugestao_emendas')
            arquivo = get_object_or_404(ArquivoBiblioteca, id=arquivo_id, mandato=user.mandato)
            dados = {
                'nome_parlamentar': user.mandato.nome_parlamentar,
                'casa_legislativa': user.mandato.get_casa_legislativa_display(),
                'esfera': {
                    user.mandato.CasaLegislativa.CM: 'Municipal',
                    user.mandato.CasaLegislativa.ALE: 'Estadual',
                    user.mandato.CasaLegislativa.CF: 'Federal',
                    user.mandato.CasaLegislativa.SENADO: 'Federal',
                }.get(user.mandato.casa_legislativa, ''),
                'municipio': user.mandato.municipio,
                'ue': user.mandato.estado,
                'temas_interesse': getattr(getattr(user.mandato, 'planejamento', None), 'temas_interesse', ''),
                'perfil_parlamentar': user.mandato.get_perfil_display(),
                'espectro_politico': user.mandato.get_posicionamento_display(),
                'origem_legislativa': 'Legislativo',
            }
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

    arquivos = ArquivoBiblioteca.objects.filter(mandato=user.mandato).order_by('-created_at')
    context = {
        'arquivos': arquivos,
        'form': form,
        'sugestoes': sugestoes,
    }
    return render(request, 'expert_pl/sugestao_emendas.html', context)
