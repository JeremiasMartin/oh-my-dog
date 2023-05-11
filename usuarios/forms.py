from django import forms
from .models import Cliente, Usuario
from django.contrib.auth.forms import UserCreationForm
import string
import random
from django.core.validators import RegexValidator

class UserSign(forms.Form):
   email = forms.EmailField(max_length=200, required=True)
   password = forms.CharField(label="Contraseña", widget=forms.PasswordInput())


class UsuarioRegistroForm(forms.ModelForm):
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput)

    class Meta:
        model = Usuario
        fields = ['email']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Las contraseñas no coinciden')
        return password2


class ClienteRegistroForm(forms.ModelForm):
    nombre = forms.CharField(validators=[RegexValidator((r'^[a-zA-Z]+$'), message="Por favor ingrese solo letras sin acentos.")])
    apellido = forms.CharField(validators=[RegexValidator((r'^[a-zA-Z]+$'), message="Por favor ingrese solo letras sin acentos.")])
    class Meta:
        model = Cliente
        fields = ['dni', 'nombre', 'apellido', 'telefono']

    def __init__(self, *args, **kwargs):
        super(ClienteRegistroForm, self).__init__(*args, **kwargs)
        self.fields['email'] = forms.EmailField(required=True)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError('Este correo electrónico ya está en uso. Prueba con otro')
        return email

    def save(self, commit=True):
        usuario = Usuario.objects.create_user(
            email=self.cleaned_data['email'],
            password=''.join(random.choices(string.ascii_letters + string.digits, k=8))  # Genera una contraseña aleatoria de 8 caracteres
        )
        cliente = super(ClienteRegistroForm, self).save(commit=False)
        cliente.user = usuario
        if commit:
            cliente.save()
        return cliente
        

class EditarPerfilForm(forms.ModelForm):
    nombre = forms.CharField(validators=[RegexValidator((r'^[a-zA-Z]+$'), message="Solo se permite el ingreso de letras")])
    apellido = forms.CharField(validators=[RegexValidator((r'^[a-zA-Z]+$'), message="Solo se permite el ingreso de letras")])
    class Meta:
        model = Cliente
        fields = ['nombre', 'apellido', 'telefono']
    def save(self, commit=True):
        cliente = super().save(commit=False)
        cliente.nombre = self.cleaned_data['nombre']
        cliente.apellido = self.cleaned_data['apellido']
        cliente.telefono = self.cleaned_data['telefono']
        if commit:
            cliente.save()
        return cliente