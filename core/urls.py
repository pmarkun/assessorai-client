from django.urls import path
from . import views
from .views import WelcomeView, MeuMandatoView, MeuPlanejamentoView, sugestao_emendas

app_name = "core"

urlpatterns = [
    path("inicio/", WelcomeView.as_view(), name="welcome"),  # Changed path to /inicio/
    path("meu-mandato/", MeuMandatoView.as_view(), name="meu_mandato"),  # Handles both create and edit
    path("meu-planejamento/", MeuPlanejamentoView.as_view(), name="meu_planejamento"),  # Handles both create and edit
    path("planejamento/", views.planejamento_wizard, name="planejamento"),
    path("equipe/", views.gestao_equipe, name="equipe"),
    path("sugestao-emendas/<int:arquivo_id>/", views.sugestao_emendas, name="sugestao_emendas"),
]

# As views podem usar @login_required e decorators de papel