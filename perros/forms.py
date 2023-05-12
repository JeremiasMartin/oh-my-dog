from django import forms
from .models import Perro, Atencion, Tipo_atencion
from django.utils.encoding import force_str
from datetime import date

class registrar_perro(forms.ModelForm):
    class Meta:
        model = Perro
        fields = ['nombre', 'raza', 'tamanio', 'fecha_nac', 'color'] 
    
        


class editar_pefil_mascota(forms.ModelForm):
    class Meta:
        model = Perro
        fields = ['nombre', 'raza', 'fecha_nac', 'color'] 
    
        
class registrar_atencion_form(forms.ModelForm):
    class Meta:
        model = Atencion
        fields = ['tipo', 'peso', 'observacion']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tipo'].label = "Tipo*"
        self.fields['tipo'].queryset = Tipo_atencion.objects.all()
        self.fields['peso'].label = "Peso*"
        self.fields['observacion'].label = force_str('Observación*')
        self.fields['observacion'].widget.attrs.update({"rows": 3})