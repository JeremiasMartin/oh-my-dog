from django.db import models
from usuarios.models import Cliente
from perros.models import Perro
# Create your models here.


class Publicacion(models.Model):
    descripcion = models.BooleanField(default=False)
    id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    id_perro_publicacion = models.ForeignKey(Perro, on_delete=models.CASCADE)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"Publicación #{self.pk}"

    class Meta:
        verbose_name = "Publicaciones"
        db_table ="Publicaciones"



from django.db import models

class PerroAdopcion(models.Model):
    SEXO_CHOICES = (
        ('M', 'Macho'),
        ('H', 'Hembra'),
    )
    TAMAÑO_CHOICES = (
        ('P', 'Pequeño'),
        ('M', 'Mediano'),
        ('G', 'Grande'),
    )
    color = models.CharField(max_length=100,blank=False)
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES,blank=False)
    tamaño = models.CharField(max_length=1, choices=TAMAÑO_CHOICES,blank=False)
    origen = models.CharField(max_length=100,blank=False)
    raza = models.CharField(max_length=100,blank=False)
    descripcion_medica = models.TextField()
    foto = models.ImageField(upload_to='adoptar_perro/', null=True, blank=True)

    def __str__(self):
        return f"{self.raza} - {self.sexo}"
    class Meta:
        verbose_name = "Perro en adopción"
        verbose_name_plural = "Perros en adopción"
        db_table = "publicaciones_perroenadopcion"