from django.forms import forms
from .models import Perro

class registrar_perro(forms.ModelForm):
    class Meta:
        model = Perro
        fields = ['nombre', 'raza', 'tamanio', 'fecha_nac', 'color']

    def save(self, commit=True):
        perro = Perro.objects.create(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password1']
        )
        cliente = super(ClienteRegistroForm, self).save(commit=False)
        cliente.user = usuario
        if commit:
            cliente.save()
        return cliente