from django import forms
from publicaciones.models import Perro_publicacion

class CruzaForm(forms.ModelForm):
    periodo_celo = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}), required=False)

    class Meta:
        model = Perro_publicacion
        fields = ('nombre', 'tamanio', 'sexo', 'color', 'edad', 'raza', 'foto')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].required = True
        self.fields['tamanio'].required = True
        self.fields['sexo'].required = True
        self.fields['color'].required = True
        self.fields['edad'].required = True
        self.fields['raza'].required = True
        self.fields['periodo_celo'].widget.attrs['style'] = 'display: none;'
        