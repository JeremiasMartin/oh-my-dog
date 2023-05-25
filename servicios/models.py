from django.db import models
from django.contrib.gis.db import models as gis_models

class Personal(models.Model):
    
    TIPO_OPCIONES = [
        ('paseador', 'Paseador'),
        ('cuidador', 'Cuidador'),
        ('guarderia', 'Guardería'),
    ]

    nombre = models.CharField(max_length=100)
    contacto = models.CharField(max_length=100)
    tipo = models.CharField(max_length=100, choices=TIPO_OPCIONES)
    direccion = models.CharField(max_length=100)
    horario = models.CharField(max_length=100)
    ubicacion = gis_models.PointField()
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'personal'
        db_table = 'servicios_personal'

    def __str__(self):
        return self.nombre

