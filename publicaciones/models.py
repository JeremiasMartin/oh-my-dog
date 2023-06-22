from django.db import models
from usuarios.models import Usuario

class Perro_publicacion(models.Model):
    nombre = models.CharField('Nombre', max_length=100, blank=True, null=True)
    opciones_tamanio = (
        ('Pequeño', 'Pequeño'),
        ('Mediano', 'Mediano'),
        ('Grande', 'Grande'),
    )
    tamanio = models.CharField('Tamaño', max_length=10, blank=False, null=False, choices=opciones_tamanio)
    SEXO_CHOICES = (
        ('M', 'Macho'),
        ('H', 'Hembra'),
    )
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES, blank=False)
    color = models.CharField('Color', max_length=100, blank=False, null=False)
    edad = models.CharField('Edad', max_length=100, blank=False, null=False)
    raza = models.CharField('Raza', max_length=100, blank=False, null=False)
    foto = models.ImageField(null=True, blank=True, upload_to='publicaciones')
    activo = models.BooleanField(default=True, editable=True)

    class Meta:
        verbose_name = 'Perro en publicación'
        db_table = 'perro_publicacion'

    def __str__(self):
        return f'Raza: {self.raza}, Tamaño: {self.tamanio}, Color: {self.color}'


class Publicacion(models.Model):
    descripcion = models.TextField(default=False, blank=True, null=True)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    id_perro_publicacion = models.OneToOneField(Perro_publicacion, on_delete=models.CASCADE)
    activo = models.BooleanField(default=True)
    tipo_publicacion = models.CharField(max_length=20, blank=False, null=False)



    def __str__(self):
        return f'{self.id_usuario}, {self.id_perro_publicacion}'

    class Meta:
        verbose_name = 'Publicación'
        db_table = 'publicaciones'


class Postulacion(models.Model):
    publicacion_adopcion = models.ForeignKey('Adopcion', on_delete=models.CASCADE, related_name='postulaciones')
    email = models.EmailField('Mail', unique=False, max_length=254, blank=True, null=False) 
    mensaje = models.TextField('Mensaje', blank=False, null=False)
    nombre = models.CharField('Nombre', max_length=20, blank=False, null=False, default='')
    apellido = models.CharField('Apellido', max_length=20, blank=False, null=False, default='')
    telefono = models.BigIntegerField('Telefono', blank=False, null=False, default=0)

    class Meta:
        db_table = 'postulaciones'


class Adopcion(models.Model):
    id_publicacion = models.ForeignKey(Publicacion, on_delete=models.CASCADE)
    origen = models.TextField(blank=False)
    motivo_adopcion = models.TextField(blank=False, null=True)
    adoptante = models.OneToOneField(Postulacion, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f'{self.id_publicacion}, Origen: {self.origen}'

    class Meta:
        verbose_name = 'Perro en adopción'
        verbose_name_plural = 'Perros en adopción'
        db_table = 'adopcion'
