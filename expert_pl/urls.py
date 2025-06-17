from django.urls import path
from . import views

app_name = 'expert_pl'

urlpatterns = [
    path('emendas/', views.sugestao_emendas, name='sugestao_emendas'),
]
