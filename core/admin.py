from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    User, Mandato, Planejamento, Objetivo, MetaObjetivo, ArquivoBiblioteca
)


# ────────────────────────────────────────────────────────────────
#  User Admin
# ────────────────────────────────────────────────────────────────
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin personalizado para o modelo User."""
    list_display = ['username', 'email', 'first_name', 'last_name', 'funcao', 'papel', 'mandato', 'is_active']
    list_filter = ['papel', 'is_active', 'is_staff', 'mandato']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'funcao']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Informações do Mandato', {
            'fields': ('funcao', 'papel', 'mandato')
        }),
    )


# ────────────────────────────────────────────────────────────────
#  Mandato Admin
# ────────────────────────────────────────────────────────────────
@admin.register(Mandato)
class MandatoAdmin(admin.ModelAdmin):
    """Admin para o modelo Mandato."""
    list_display = ['nome_parlamentar', 'cargo', 'casa_legislativa', 'estado', 'municipio', 'posicionamento', 'primeiro_mandato']
    list_filter = ['cargo', 'casa_legislativa', 'estado', 'posicionamento', 'perfil', 'primeiro_mandato']
    search_fields = ['nome_parlamentar', 'estado', 'municipio']
    ordering = ['nome_parlamentar']


# ────────────────────────────────────────────────────────────────
#  Planejamento Admin
# ────────────────────────────────────────────────────────────────
class ObjetivoInline(admin.TabularInline):
    """Inline para objetivos dentro do planejamento."""
    model = Objetivo
    extra = 1
    fields = ['descricao', 'ordem']


@admin.register(Planejamento)
class PlanejamentoAdmin(admin.ModelAdmin):
    """Admin para o modelo Planejamento."""
    list_display = ['mandato', 'objetivo_ano', 'created_at']
    list_filter = ['created_at', 'mandato__casa_legislativa']
    search_fields = ['mandato__nome_parlamentar', 'objetivo_ano']
    inlines = [ObjetivoInline]
    
    fieldsets = (
        ('Mandato', {
            'fields': ('mandato',)
        }),
        ('Análise Estratégica', {
            'fields': ('oportunidades', 'fraquezas', 'temas_interesse')
        }),
        ('Objetivo Principal', {
            'fields': ('objetivo_ano',)
        }),
    )


# ────────────────────────────────────────────────────────────────
#  Objetivo Admin
# ────────────────────────────────────────────────────────────────
class MetaObjetivoInline(admin.TabularInline):
    """Inline para metas dentro do objetivo."""
    model = MetaObjetivo
    extra = 1
    fields = ['indicador', 'valor_alvo', 'valor_atual', 'data_limite']


@admin.register(Objetivo)
class ObjetivoAdmin(admin.ModelAdmin):
    """Admin para o modelo Objetivo."""
    list_display = ['descricao', 'planejamento', 'ordem']
    list_filter = ['planejamento__mandato']
    search_fields = ['descricao', 'planejamento__mandato__nome_parlamentar']
    ordering = ['planejamento', 'ordem']
    inlines = [MetaObjetivoInline]


# ────────────────────────────────────────────────────────────────
#  Meta Objetivo Admin
# ────────────────────────────────────────────────────────────────
@admin.register(MetaObjetivo)
class MetaObjetivoAdmin(admin.ModelAdmin):
    """Admin para o modelo MetaObjetivo."""
    list_display = ['indicador', 'objetivo', 'valor_atual', 'valor_alvo', 'data_limite']
    list_filter = ['data_limite', 'objetivo__planejamento__mandato']
    search_fields = ['indicador', 'objetivo__descricao']
    ordering = ['objetivo', 'indicador']


# ────────────────────────────────────────────────────────────────
#  Arquivo Biblioteca Admin
# ────────────────────────────────────────────────────────────────
@admin.register(ArquivoBiblioteca)
class ArquivoBibliotecaAdmin(admin.ModelAdmin):
    """Admin para o modelo ArquivoBiblioteca."""
    list_display = ['titulo', 'tipo', 'mandato', 'created_at']
    list_filter = ['tipo', 'created_at', 'mandato']
    search_fields = ['titulo', 'mandato__nome_parlamentar']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('titulo', 'tipo', 'mandato')
        }),
        ('Arquivo', {
            'fields': ('arquivo',)
        }),
    )
