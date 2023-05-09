from django import forms
from .models import Turno

class SolicitarTurnoForm(forms.ModelForm):
    class Meta:
        model = Turno
        fields = ['fecha', 'tipo_atencion', 'estado']
