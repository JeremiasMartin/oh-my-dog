
from django import forms
from .models import Perro_publicacion, Publicacion
from .models import Postulacion

class AdopcionForm(forms.ModelForm):
    origen = forms.CharField(max_length=100, widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}))
    motivo_adopcion = forms.CharField(max_length=100, widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}))

    class Meta:
        model = Perro_publicacion
        fields = ('nombre', 'tamanio', 'sexo', 'color', 'edad', 'raza')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].required = False
        self.fields['tamanio'].required = True
        self.fields['sexo'].required = True
        self.fields['color'].required = True
        self.fields['edad'].required = True
        self.fields['raza'].required = True
        
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if nombre is not None and nombre.strip() == '':
            return None  # Si el nombre está vacío, se establece como None
        return nombre


class PostulacionForm(forms.ModelForm):
    class Meta:
        model = Postulacion
        fields = ['nombre', 'apellido', 'email', 'telefono', 'mensaje']
        exclude = []

    def __init__(self, *args, **kwargs):
        esRegistrado = kwargs.pop('esRegistrado', False)
        super(PostulacionForm, self).__init__(*args, **kwargs)

        if esRegistrado:
            self.fields.pop('nombre')
            self.fields.pop('apellido')
            self.fields.pop('telefono')


class EditarAdopcionForm(forms.ModelForm):
    origen = forms.CharField(max_length=100, widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}))
    motivo_adopcion = forms.CharField(max_length=100, widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}))
    class Meta:
        model = Perro_publicacion
        fields = ['nombre', 'tamanio', 'sexo', 'color', 'edad', 'raza']
