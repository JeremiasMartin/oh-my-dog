from django import forms
from .models import Adopcion

class AdopcionForm(forms.ModelForm):
    class Meta:
        model = Adopcion
        fields = ('perro_publicacion', 'origen', 'motivo_adopcion')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['perro_publicacion'].required = True
        self.fields['origen'].required = True
        self.fields['motivo_adopcion'].required = True