from django.db import models
from publicaciones.models import Publicacion


class Cruza(models.Model):
    publicacion = models.ForeignKey(Publicacion, on_delete=models.CASCADE)

    def __str__(self):
        return f'Perro {self.publicacion__id_perro_publicacion__nombre} de {self.publicacion__id_usuario}'

    class Meta:
        verbose_name = 'Cruza'
        db_table = 'cruza'
