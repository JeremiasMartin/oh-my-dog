from django import forms
from .models import Turno
from perros.models import Perro
from django import forms
from django.forms.widgets import DateInput
from datetime import date


class SolicitarTurnoForm(forms.ModelForm):
    def __init__(self, cliente,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['perro'].choices = self.opciones_perros(cliente)

    def opciones_perros(self, cliente):
        perros = Perro.objects.filter(cliente=cliente)
        opciones = [perro.nombre for perro in perros]
        opciones.append("No Registrada")
        return opciones
    
    
    class Meta:
        model = Turno
        fields = ['fecha', 'tipo_atencion','perro']
        widgets = {
            'fecha': DateInput(attrs={'type': 'date','min': str(date.today())}),
        }
        
        