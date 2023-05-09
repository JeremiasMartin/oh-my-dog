from django.db import models
from usuarios.models import Cliente

class Turno(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    tipo_atencion=models.ForeignKey(TipoAtencion,on_delete=models.CASCADE)
    fecha = models.DateTimeField()
    estado = models.ForeignKey(EstadoTurno, on_delete=models.CASCADE)




class EstadoTurno(models.Model):
    ESTADOS_TURNO = [
        ('ACEPTADO', 'Aceptado'),                     
        ('RECHAZADO', 'Rechazado'), 
        ('PENDIENTE', 'Pendiente'),
    ]
    estado = models.CharField(max_length=10, choices=ESTADOS_TURNO)

    def __str__(self):
        return self.estado
  
  