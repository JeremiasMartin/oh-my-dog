from django.db import models
from OhMyDog import settings
from usuarios.models import Cliente

class Perro(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, blank=False, null=False)
    nombre = models.CharField('Nombre', max_length=100, blank=False, null=False)
    raza = models.CharField('Raza', max_length=100, blank=False, null=False)

    opciones_tamanio = (
        ('Pequeño','Pequeño'),
        ('Mediano','Mediano'),
        ('Grande','Grande'),
    )
    tamanio = models.CharField('Tamanio', max_length=10, blank=False, null=False, choices= opciones_tamanio)
    fecha_nac = models.DateField('Nacimiento', blank=False, null=False)
    color = models.CharField('Color', max_length=100, blank=False, null=False)

    class Meta:
        verbose_name = 'perro'
        db_table = 'perros'

    def __str__(self) -> str:
        return '%s, %s, %s' % (self.nombre, self.raza, self.tamanio)

class Tipo_atencion(models.Model):
    tipos = (
        ('Vacuna antiviral A','Vacuna antiviral A' ),
        ('Vacuna antiviral B','Vacuna antiviral B'),
        ('Castración','Castración'),
        ('Vacuna Desparasitante', 'Vacuna Desparasitante'),
        ('Atención Clínica','Atención Clínica'),
    )
    tipo = models.CharField('Tipo', unique=True, max_length=25, blank=False, null=False, choices=tipos)

    class Meta:
        verbose_name = 'tipo'
        db_table = 'tipos_atencion'
    
    def __str__(self) -> str:
        return '%s' % (self.tipo)

class Atencion(models.Model):
    mascota = models.ForeignKey(Perro, on_delete=models.CASCADE)
    tipo = models.ForeignKey(Tipo_atencion, on_delete=models.CASCADE)
    peso = models.DecimalField('Peso', max_digits=5, decimal_places=2, blank=False, null=False)
    fecha = models.DateField('Fecha', blank=False, null=False)
    observacion = models.TextField('Observacion', blank=False, null=True)

    class Meta:
        verbose_name = 'atencione'
        db_table = 'atenciones'
    
    def __str__(self) -> str:
        return '%s, %s' % (self.fecha, self.id_tipo)







