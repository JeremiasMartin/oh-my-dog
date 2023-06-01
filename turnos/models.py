from django.db import models
from usuarios.models import Cliente
from perros.forms import Tipo_atencion


class EstadoTurno(models.Model):
    ESTADOS_TURNO = [
        ('ACEPTADO', 'Aceptado'),                     
        ('RECHAZADO', 'Rechazado'), 
        ('PENDIENTE', 'Pendiente'),
    ]
    estado = models.CharField(max_length=10, choices=ESTADOS_TURNO)

    def __str__(self):
        return self.estado
  


class Turno(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    tipo_atencion=models.ForeignKey(Tipo_atencion,on_delete=models.CASCADE)
    fecha = models.DateTimeField()
    estado = models.ForeignKey(EstadoTurno, on_delete=models.CASCADE)
    perro = models.CharField('Perro', max_length=20, blank=False, null=False, default='')

    def __str__(self):
        return f"Turno de {self.usuario} para {self.tipo_servicio} el día {self.fecha}"
  