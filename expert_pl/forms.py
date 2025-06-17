from django import forms
from core.models import ArquivoBiblioteca

class ArquivoBibliotecaForm(forms.ModelForm):
    class Meta:
        model = ArquivoBiblioteca
        fields = ['titulo', 'tipo', 'arquivo']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500'
            })
