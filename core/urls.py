from django.urls import path
from . import views
from .views import WelcomeView, MeuMandatoView, MeuPlanejamentoView

app_name = "core"

urlpatterns = [
    path("inicio/", WelcomeView.as_view(), name="welcome"),  # Changed path to /inicio/
    path("meu-mandato/", MeuMandatoView.as_view(), name="meu_mandato"),  # Handles both create and edit
    path("meu-planejamento/", MeuPlanejamentoView.as_view(), name="meu_planejamento"),  # Handles both create and edit
    path("planejamento/", views.planejamento_wizard, name="planejamento"),
    path("equipe/", views.gestao_equipe, name="equipe"),
]

# As views podem usar @login_required e decorators de papel