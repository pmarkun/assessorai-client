from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Row, Column, HTML
from .models import Mandato, Planejamento, Objetivo

class MandatoForm(forms.ModelForm):
    class Meta:
        model = Mandato
        fields = [
            'nome_parlamentar',
            'casa_legislativa',
            'cargo', 
            'estado',
            'municipio',
            'posicionamento',
            'perfil',
            'primeiro_mandato'
        ]
        labels = {
            'nome_parlamentar': 'Nome Parlamentar',
            'casa_legislativa': 'Casa Legislativa',
            'cargo': 'Cargo',
            'estado': 'Estado',
            'municipio': 'Município',
            'posicionamento': 'Posicionamento Político',
            'perfil': 'Perfil Parlamentar',
            'primeiro_mandato': 'É seu primeiro mandato?'
        }
        help_texts = {
            'nome_parlamentar': 'Como você é conhecido(a) politicamente',
            'casa_legislativa': 'Escolha a casa legislativa onde exerce seu mandato',
            'municipio': 'Preencha apenas se for vereador(a)',
            'posicionamento': 'Seu posicionamento no espectro político (opcional)',
            'perfil': 'Qual o seu principal perfil de atuação? (opcional)',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            HTML('<div class="mb-6"><h2 class="text-xl font-semibold text-gray-800 mb-2">Informações Básicas</h2></div>'),
            Fieldset(
                '',
                Row(
                    Column('nome_parlamentar', css_class='form-group w-full mb-4'),
                    css_class='form-row grid grid-cols-1 md:grid-cols-2 gap-4'
                ),
                Row(
                    Column('casa_legislativa', css_class='form-group w-full md:w-1/2'),
                    Column('cargo', css_class='form-group w-full md:w-1/2'),
                    css_class='form-row grid grid-cols-1 md:grid-cols-2 gap-4'
                ),
                Row(
                    Column('estado', css_class='form-group w-full md:w-1/2'),
                    Column('municipio', css_class='form-group w-full md:w-1/2'),
                    css_class='form-row grid grid-cols-1 md:grid-cols-2 gap-4'
                ),
                css_class='mb-6'
            ),
            HTML('<div class="mb-6"><h2 class="text-xl font-semibold text-gray-800 mb-2">Perfil Político</h2></div>'),
            Fieldset(
                '',
                Row(
                    Column('posicionamento', css_class='form-group w-full md:w-1/2'),
                    Column('perfil', css_class='form-group w-full md:w-1/2'),
                    css_class='form-row grid grid-cols-1 md:grid-cols-2 gap-4'
                ),
                Row(
                    Column('primeiro_mandato', css_class='form-group w-full'),
                    css_class='form-row grid grid-cols-1 md:grid-cols-2 gap-4'
                ),
                css_class='mb-6'
            )
        )

        # Make municipio field conditional based on cargo
        self.fields['municipio'].required = False
        
        # Add CSS classes for better styling
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs.update({
                    'class': 'block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500'
                })
            elif isinstance(field.widget, forms.TextInput):
                label = field.label or field_name.replace('_', ' ').title()
                field.widget.attrs.update({
                    'class': 'block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500',
                    'placeholder': f'Digite {label.lower()}'
                })
            elif isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({
                    'class': 'h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded'
                })

    def clean(self):
        cleaned_data = super().clean()
        cargo = cleaned_data.get('cargo')
        municipio = cleaned_data.get('municipio')
        casa_legislativa = cleaned_data.get('casa_legislativa')

        # Validate that municipio is provided for vereador
        if cargo == Mandato.Cargo.VEREADOR and not municipio:
            raise forms.ValidationError('Município é obrigatório para vereadores.')
        
        # Validate cargo/casa_legislativa consistency
        cargo_casa_map = {
            Mandato.Cargo.VEREADOR: Mandato.CasaLegislativa.CM,
            Mandato.Cargo.DEP_ESTADUAL: Mandato.CasaLegislativa.ALE,
            Mandato.Cargo.DEP_FEDERAL: Mandato.CasaLegislativa.CF,
            Mandato.Cargo.SENADOR: Mandato.CasaLegislativa.SENADO,
        }
        
        if cargo and casa_legislativa:
            expected_casa = cargo_casa_map.get(cargo)
            if expected_casa and casa_legislativa != expected_casa:
                raise forms.ValidationError(
                    f'O cargo {cargo} deve estar associado à {expected_casa}.'
                )

        return cleaned_data


class PlanejamentoForm(forms.ModelForm):
    class Meta:
        model = Planejamento
        fields = [
            'oportunidades',
            'fraquezas', 
            'temas_interesse',
            'objetivo_ano'
        ]
        labels = {
            'oportunidades': 'Oportunidades',
            'fraquezas': 'Ameaças',
            'temas_interesse': 'Temas Prioritários',
            'objetivo_ano': 'Objetivo do Ano'
        }
        help_texts = {
            'oportunidades': 'Quais as principais oportunidades políticas que hoje podem ser aproveitadas pelo seu mandato?',
            'fraquezas': 'Quais as principais barreiras políticas, partidárias e da equipe que impedem o sucesso do seu mandato?',
            'temas_interesse': 'Liste os temas que são prioritários para seu mandato (máximo 3 temas)',
            'objetivo_ano': 'Qual o principal objetivo que você quer alcançar este ano?'
        }
        widgets = {
            'oportunidades': forms.Textarea(attrs={'rows': 4, 'maxlength': 500}),
            'fraquezas': forms.Textarea(attrs={'rows': 4, 'maxlength': 500}),
            'temas_interesse': forms.Textarea(attrs={'rows': 3, 'maxlength': 300}),
            'objetivo_ano': forms.TextInput(attrs={'maxlength': 255})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            HTML('<div class="mb-6"><h2 class="text-xl font-semibold text-gray-800 mb-4">Análise Estratégica</h2><p class="text-gray-600 mb-4">A AssessorAI pode sugerir objetivos e metas para uma atuação mais efetiva</p></div>'),
            Fieldset(
                '',
                Row(
                    Column('oportunidades', css_class='form-group w-full md:w-1/2'),
                    Column('fraquezas', css_class='form-group w-full md:w-1/2'),
                    css_class='form-row grid grid-cols-1 md:grid-cols-2 gap-4'
                ),
                Row(
                    Column('temas_interesse', css_class='form-group w-full'),
                    css_class='form-row grid grid-cols-1 md:grid-cols-2 gap-4'
                ),
                css_class='mb-6'
            ),
            HTML('<div class="mb-6"><h2 class="text-xl font-semibold text-gray-800 mb-4">Objetivo Principal</h2></div>'),
            Fieldset(
                '',
                Row(
                    Column('objetivo_ano', css_class='form-group w-full'),
                    css_class='form-row grid grid-cols-1 md:grid-cols-2 gap-4'
                ),
                css_class='mb-6'
            )
        )

        # Add CSS classes for better styling
        for field_name, field in self.fields.items():
            label = field.label or field_name.replace('_', ' ').title()
            if isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({
                    'class': 'block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 resize-none',
                    'placeholder': field.help_text or f'Descreva {label.lower()}'
                })
            elif isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({
                    'class': 'block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500',
                    'placeholder': field.help_text or f'Digite {label.lower()}'
                })


class ObjetivoForm(forms.ModelForm):
    class Meta:
        model = Objetivo
        fields = ['descricao']
        labels = {
            'descricao': 'Descrição do Objetivo'
        }
        widgets = {
            'descricao': forms.TextInput(attrs={'maxlength': 255})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['descricao'].widget.attrs.update({
            'class': 'block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500',
            'placeholder': 'Digite uma meta específica para seu objetivo principal'
        })
