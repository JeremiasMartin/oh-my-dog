from django.db import models
from django.contrib.gis.db import models as gis_models

class Personal(models.Model):
    
    TIPO_OPCIONES = [
        ('paseador', 'Paseador'),
        ('cuidador', 'Cuidador'),
        ('guarderia', 'Guardería'),
    ]

    nombre = models.CharField(max_length=100, blank=False, null=False, default='')
    email = models.EmailField('Mail', max_length=254, blank=True, null=False) 
    telefono = models.BigIntegerField('Telefono', blank=False, null=False, default='')
    tipo = models.CharField(max_length=200,blank=False, null=False, default='', choices=TIPO_OPCIONES)
    descripcion = models.CharField(max_length=200, blank=False, null=False, default='')
    horario = models.CharField(max_length=200, blank=False, null=False, default='')
    ubicacion = gis_models.PointField()
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'personal'
        db_table = 'servicios_personal'

    def __str__(self):
        return self.nombre

