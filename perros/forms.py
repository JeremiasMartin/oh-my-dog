from django import forms
from .models import Perro

class registrar_perro(forms.ModelForm):
    class Meta:
        model = Perro
        fields = ['nombre', 'raza', 'tamanio', 'fecha_nac', 'color']  