from django.db import models
from publicaciones.models import Publicacion

class Postulacion(models.Model):
    publicacion = models.ForeignKey(Publicacion, on_delete=models.CASCADE, related_name='publicacion')
    publicacion_postulante = models.ForeignKey(Publicacion, on_delete=models.CASCADE, related_name='postulante')
    match= models.BooleanField(default=False)
    fecha_match = models.DateField('Fecha', blank=True, null=True)
    
    class Meta:
        db_table = 'postulaciones_cruza'