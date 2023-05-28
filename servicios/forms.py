from django import forms
from django.contrib.gis import forms as gis_forms
from leaflet.forms.widgets import LeafletWidget
from .models import Personal

class PersonalForm(forms.ModelForm):
    ubicacion = gis_forms.PointField(widget=LeafletWidget())

    class Meta:
        model = Personal
        fields = ('nombre', 'contacto', 'tipo', 'direccion', 'horario', 'ubicacion', 'activo')

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
        fields = ('nombre', 'contacto', 'tipo', 'direccion', 'horario', 'ubicacion')
    
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