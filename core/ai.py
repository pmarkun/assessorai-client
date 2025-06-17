try:
    import openai
except ImportError:  # pragma: no cover - library optional
    openai = None
from .models import AISettings, Mandato


def _get_settings():
    return AISettings.get_solo()


def suggest_positions(num_positions: int, mandato: Mandato) -> str:
    settings = _get_settings()
    if openai is None or not settings.api_key:
        return "Configurar chave de API para obter sugestões."
    openai.api_key = settings.api_key
    prompt = (
        "Considere a seguinte estrutura de equipe do mandato: "
        f"{', '.join(mandato.usuarios.values_list('funcao', flat=True))}. "
        f"Sugira {num_positions} cargos e atribuições complementares."
    )
    response = openai.ChatCompletion.create(
        model=settings.model_name,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content.strip()


def suggest_tasks(cargo: str, mandato: Mandato) -> str:
    settings = _get_settings()
    if openai is None or not settings.api_key:
        return "Configurar chave de API para obter sugestões."
    openai.api_key = settings.api_key
    prompt = (
        f"Considerando um mandato parlamentar, sugira atividades e escopo para o cargo '{cargo}'."
    )
    response = openai.ChatCompletion.create(
        model=settings.model_name,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content.strip()
