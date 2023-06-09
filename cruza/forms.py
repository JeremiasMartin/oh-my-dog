from django import forms
from publicaciones.models import Perro_publicacion

class CustomImageWidget(forms.ClearableFileInput):
    def render(self, name, value, attrs=None, renderer=None):
        return super().render(name, value, attrs=attrs, renderer=renderer)

class CruzaForm(forms.ModelForm):
    periodo_celo = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}), required=False)
    foto = forms.ImageField(widget=CustomImageWidget, required=True)
    edad = forms.CharField(widget=forms.NumberInput(attrs={'type': 'number', 'min': '1'}))

    class Meta:
        model = Perro_publicacion
        fields = ('nombre', 'tamanio', 'sexo', 'color', 'edad', 'raza')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].required = True
        self.fields['tamanio'].required = True
        self.fields['sexo'].required = True
        self.fields['color'].required = True
        self.fields['edad'].required = True
        self.fields['raza'].required = True
        self.fields['periodo_celo'].widget.attrs['style'] = 'display: none;'