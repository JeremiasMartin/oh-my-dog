
from django import forms
from .models import Perro_publicacion, Publicacion
from .models import Postulacion, PostulacionPerdidosEncontrados

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
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.tipo_publicacion = 'Adopcion'

        if commit:
            instance.save()
            publicacion = Publicacion.objects.create(
                descripcion=self.cleaned_data['motivo_adopcion'],
                id_perro_publicacion=instance,
                tipo_publicacion='Adopcion',
                activo=True
            )

        return instance

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


class PublicarPerroPerdidoForm(forms.Form):
    
    nombre = forms.CharField(max_length=100)
    tamanio = forms.ChoiceField(choices=Perro_publicacion.opciones_tamanio)
    sexo = forms.ChoiceField(choices=Perro_publicacion.SEXO_CHOICES)
    color = forms.CharField(max_length=100)
    edad = forms.CharField(max_length=100)
    raza = forms.CharField(max_length=100)
    foto = forms.ImageField()
    descripcion = forms.CharField(widget=forms.Textarea)
    tipo_publicacion = forms.CharField(max_length=20, initial='Perdidos', widget=forms.HiddenInput)

    def save(self, user):
        perro_perdido = Perro_publicacion.objects.create(
            nombre=self.cleaned_data['nombre'],
            tamanio=self.cleaned_data['tamanio'],
            sexo=self.cleaned_data['sexo'],
            color=self.cleaned_data['color'],
            edad=self.cleaned_data['edad'],
            raza=self.cleaned_data['raza'],
            foto=self.cleaned_data['foto']
        )

        publicacion = Publicacion.objects.create(
            descripcion=self.cleaned_data['descripcion'],
            id_usuario=user,
            id_perro_publicacion=perro_perdido,
            tipo_publicacion=self.cleaned_data['tipo_publicacion']
        )

class CargarPerroEncontradoForm(forms.Form):
    nombre = forms.CharField(max_length=100, required=False)
    tamanio = forms.ChoiceField(choices=Perro_publicacion.opciones_tamanio)
    sexo = forms.ChoiceField(choices=Perro_publicacion.SEXO_CHOICES)
    color = forms.CharField(max_length=100)
    edad_aproximada = forms.CharField(max_length=100)
    raza = forms.CharField(max_length=100)
    descripcion = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}))
    foto = forms.ImageField()

    def save(self, user):
        perro_publicacion = Perro_publicacion.objects.create(
            nombre=self.cleaned_data['nombre'],
            tamanio=self.cleaned_data['tamanio'],
            sexo=self.cleaned_data['sexo'],
            color=self.cleaned_data['color'],
            edad=self.cleaned_data['edad_aproximada'],
            raza=self.cleaned_data['raza'],
            foto=self.cleaned_data['foto'],
            activo=True
        )

        publicacion = Publicacion.objects.create(
            descripcion=self.cleaned_data['descripcion'],
            id_usuario=user,
            id_perro_publicacion=perro_publicacion,
            activo=True,
            tipo_publicacion='Encontrado'
        )



class PostulacionPerrosForm(forms.ModelForm):
    class Meta:
        model = PostulacionPerdidosEncontrados
        fields = ['nombre', 'apellido', 'email', 'telefono', 'mensaje']
        exclude = []

    def __init__(self, *args, **kwargs):
        esRegistrado = kwargs.pop('esRegistrado', False)
        super().__init__(*args, **kwargs)

        if not esRegistrado:
            self.fields['nombre'].required = True
            self.fields['apellido'].required = True
            self.fields['telefono'].required = True
