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

    def __str__(self):
        return f'{self.id_usuario}, {self.id_perro_publicacion}'

    class Meta:
        verbose_name = 'Publicación'
        db_table = 'publicaciones'


class Adopcion(models.Model):
    id_publicacion = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    perro_publicacion = models.ForeignKey(Perro_publicacion, on_delete=models.CASCADE)
    origen = models.TextField(blank=False)
    motivo_adopcion = models.TextField(blank=False, null=True)

    def __str__(self):
        return f'{self.id_publicacion}, Origen: {self.origen}'

    class Meta:
        verbose_name = 'Perro en adopción'
        verbose_name_plural = 'Perros en adopción'
        db_table = 'adopcion'



class Postulacion(models.Model):
    cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='postulaciones')
    publicacion_adopcion = models.ForeignKey(Adopcion, on_delete=models.CASCADE, related_name='postulaciones')
    email = models.EmailField(blank=False, null=False)
    mensaje = models.TextField(blank=False, null=False)
    nombre = models.CharField(max_length=100, blank=False, null=False)
    telefono = models.CharField(max_length=20, blank=False, null=False)
    class Meta:
        db_table = 'postulaciones'
