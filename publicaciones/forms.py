
from django import forms
from .models import PerroAdopcion

class AdopcionForm(forms.ModelForm):
    class Meta:
        model = PerroAdopcion
        fields = ('sexo', 'tamaño', 'color', 'origen', 'raza', 'descripcion_medica', 'foto')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['color'].required = True
        self.fields['sexo'].required = True
        self.fields['tamaño'].required = True
        self.fields['origen'].required = True
        self.fields['raza'].required = True
        self.fields['descripcion_medica'].required = True