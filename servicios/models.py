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

class Guardia(models.Model):
    descripcion = models.TextField()

    class Meta:
        verbose_name = 'guardias'
        db_table = 'servicios_guardias'

class Campaña(models.Model):
    nombre = models.CharField(max_length=100, blank=False, null=False, default='')
    motivo = models.CharField(max_length=300, blank=False, null=False, default='')
    objetivo = models.IntegerField(blank=False, null=False)
    recaudado = models.IntegerField(blank=False, null=False , default=0)
    fechaInicio = models.DateField(blank=False, null=False)
    fechaFin = models.DateField(blank=False, null=False)

    class Meta:
        verbose_name = 'campañas'
        db_table = 'servicios_campañas'


class Donacion(models.Model):
    nombre = models.CharField(max_length=100, blank=True, null=True, default='')
    apellido = models.CharField(max_length=100, blank=True, null=True, default='')
    email = models.EmailField('Mail', max_length=254, blank=True, null=False) 
    monto = models.IntegerField(blank=False, null=False)
    fecha = models.DateField(blank=False, null=False)
    campaña = models.ForeignKey(Campaña, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'donaciones'
        db_table = 'servicios_donaciones'

