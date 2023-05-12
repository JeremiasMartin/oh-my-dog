from django import forms
from .models import Turno
from django import forms
from django.forms.widgets import DateInput
from datetime import date


class SolicitarTurnoForm(forms.ModelForm):
    class Meta:
        model = Turno
        fields = ['fecha', 'tipo_atencion', 'estado']
        widgets = {
            'fecha': DateInput(attrs={'type': 'date','min': str(date.today())})
        }
        
        