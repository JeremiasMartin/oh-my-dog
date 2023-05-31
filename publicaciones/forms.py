
from django import forms
from .models import Perro_publicacion, Adopcion

class AdopcionForm(forms.ModelForm):
    foto = forms.ImageField(required=True)
    origen = forms.CharField(max_length=100, widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}))
    motivo_adopcion = forms.CharField(max_length=100, widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}))

    class Meta:
        model = Perro_publicacion
        fields = ('nombre', 'tamanio', 'sexo', 'color', 'edad', 'raza', 'foto')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].required = True
        self.fields['tamanio'].required = True
        self.fields['sexo'].required = True
        self.fields['color'].required = True
        self.fields['edad'].required = True
        self.fields['raza'].required = True
        self.fields['foto'].required = True
