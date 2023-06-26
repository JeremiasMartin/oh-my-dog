from django import forms
from django.contrib.gis import forms as gis_forms
from leaflet.forms.widgets import LeafletWidget
from .models import Personal
from .models import Guardia
from .models import Campaña

class PersonalForm(forms.ModelForm):
    ubicacion = gis_forms.PointField(widget=LeafletWidget())

    class Meta:
        model = Personal
        fields = ('nombre', 'email', 'telefono', 'tipo', 'descripcion', 'horario', 'ubicacion')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['ubicacion'].required = False
    
    def clean_ubicacion(self):
        ubicacion = self.cleaned_data.get('ubicacion')
        if not ubicacion:
            raise forms.ValidationError('Debe seleccionar una ubicación en el mapa.')
        return ubicacion

    def save(self, commit=True):
        personal = super().save(commit=False)
        coordenadas = self.cleaned_data.get('ubicacion')
        if coordenadas:
            personal.ubicacion = coordenadas
        if commit:
            personal.save()
        return personal
    
class PersonalEditForm(forms.ModelForm):
    
    ubicacion = gis_forms.PointField(widget=LeafletWidget())

    class Meta:
        model = Personal
        fields = ('nombre', 'email', 'telefono', 'tipo', 'descripcion', 'horario', 'ubicacion')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['ubicacion'].required = False
    
    def clean_ubicacion(self):
        ubicacion = self.cleaned_data.get('ubicacion')
        if not ubicacion:
            raise forms.ValidationError('Debe seleccionar una ubicación en el mapa.')
        return ubicacion
    
    def save(self, commit=True):
        personal = super().save(commit=False)
        coordenadas = self.cleaned_data.get('ubicacion')
        if coordenadas:
            personal.ubicacion = coordenadas
        if commit:
            personal.save()
        return personal
    
class GuardiaForm(forms.ModelForm):
    
    class Meta:
        model = Guardia
        fields = ('descripcion',)
    
    def save(self, commit=True):
        guardia = super().save(commit=False)
        if commit:
            guardia.save()
        return guardia
    
class CampañaForm(forms.ModelForm):
    
    class Meta:
        model = Campaña
        fields = ('nombre', 'motivo', 'fechaInicio', 'fechaFin')
    
    def save(self, commit=True):
        campaña = super().save(commit=False)
        if commit:
            campaña.save()
        return campaña