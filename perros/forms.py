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
    tipo = forms.ModelChoiceField(queryset=Tipo_atencion.objects.all(), empty_label=None)
    peso = forms.DecimalField(validators=[MinValueValidator(0)])
    class Meta:
        model = Atencion
        fields = ['tipo', 'peso', 'observacion']