from django.db import models
from usuarios.models import Cliente
from django.core.validators import MaxValueValidator, RegexValidator, MinValueValidator
from datetime import date

class Perro(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, blank=False, null=False)
    nombre = models.CharField('Nombre', validators = [RegexValidator((r'^[a-zA-Z ]+$'), message="Por favor ingrese solo letras sin acentos.")], 
                              max_length=100, blank=False, null=False)
    raza = models.CharField('Raza', max_length=100, validators = [RegexValidator((r'^[a-zA-Z ]+$'), message="Por favor ingrese solo letras sin acentos.")],
                            blank=False, null=False)

    opciones_tamanio = (
        ('Pequeño','Pequeño'),
        ('Mediano','Mediano'),
        ('Grande','Grande'),
    )
    tamanio = models.CharField('Tamanio', max_length=10, blank=False, null=False, choices= opciones_tamanio)
    fecha_nac = models.DateField('Nacimiento',
                                 validators=[MaxValueValidator((date.today), message="La fecha ingresada no puede ser futura")], 
                                 blank=False, null=False)
    color = models.CharField('Color', validators = [RegexValidator((r'^[a-zA-Z ]+$'), message="Por favor ingrese solo letras sin acentos.")],
                             max_length=100, blank=False, null=False)

    class Meta:
        verbose_name = 'perro'
        db_table = 'perros'

    def __str__(self) -> str:
        return '%s, %s, %s' % (self.nombre, self.raza, self.tamanio)

class Tipo_atencion(models.Model):
    tipos = (
        ('Vacuna antiviral','Vacuna antiviral' ),
        ('Vacuna antirrábica','Vacuna antirrábica'),
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
    peso = models.DecimalField('Peso', validators = [MinValueValidator(0)],
                               max_digits=5, decimal_places=2, blank=False, null=False)
    fecha = models.DateField('Fecha', blank=False, null=False)
    observacion = models.TextField('Observacion', blank=False, null=True)

    class Meta:
        verbose_name = 'atencione'
        db_table = 'atenciones'
    
    def __str__(self) -> str:
        return '%s, %s' % (self.fecha, self.id_tipo)







