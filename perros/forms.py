from django import forms
from .models import Perro, Atencion, Tipo_atencion
from django.core.validators import RegexValidator, MinValueValidator

class registrar_perro(forms.ModelForm):
    nombre = forms.CharField(validators=[RegexValidator((r'^[a-zA-Z ]+$'), message="Por favor ingrese solo letras sin acentos.")])
    raza = forms.CharField(validators=[RegexValidator((r'^[a-zA-Z ]+$'), message="Por favor ingrese solo letras sin acentos.")])
    color = forms.CharField(validators=[RegexValidator((r'^[a-zA-Z ]+$'), message="Por favor ingrese solo letras sin acentos.")])
    class Meta:
        model = Perro
        fields = ['nombre', 'raza', 'tamanio', 'fecha_nac', 'color']  

class editar_pefil_mascota(forms.ModelForm):
    nombre = forms.CharField(validators=[RegexValidator((r'^[a-zA-Z ]+$'), message="Por favor ingrese solo letras sin acentos.")])
    raza = forms.CharField(validators=[RegexValidator((r'^[a-zA-Z ]+$'), message="Por favor ingrese solo letras sin acentos.")])
    color = forms.CharField(validators=[RegexValidator((r'^[a-zA-Z ]+$'), message="Por favor ingrese solo letras sin acentos.")])
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
        self.fields['peso'].validators = [MinValueValidator(0)]
        self.fields['observacion'].label = "Observacion*"
        self.fields['observacion'].widget.attrs.update({"rows": 3})