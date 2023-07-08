from django import forms
from django.contrib.gis import forms as gis_forms
from leaflet.forms.widgets import LeafletWidget
from .models import Personal
from .models import Guardia
from .models import Campaña
from .models import Donacion
from django.forms.widgets import DateInput

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
        fields = ('fecha','veterinaria')
    
class CampañaForm(forms.ModelForm):

    class Meta:
        model = Campaña
        fields = ('nombre', 'motivo', 'objetivo', 'fechaInicio', 'fechaFin')
        labels = {
            'fechaInicio': 'Fecha de Inicio',
            'fechaFin': 'Fecha de Fin',
        }
        widgets = {
            'fechaInicio': DateInput(attrs={'type': 'date'}),
            'fechaFin': DateInput(attrs={'type': 'date'}),
        }

        
    def save(self, commit=True):
        campaña = super().save(commit=False)
        if commit:
            campaña.save()
        return campaña
    
class DonacionForm(forms.ModelForm):
        
        class Meta:
            model = Donacion
            fields = ('email', 'monto')

        def __init__(self, *args, **kwargs):
            user = kwargs.pop('user', None)
            super().__init__(*args, **kwargs)
            if user and user.is_authenticated:
                del self.fields['email']    
        
        def save(self, commit=True):
            donacion = super().save(commit=False)
            if commit:
                donacion.save()
            return donacion