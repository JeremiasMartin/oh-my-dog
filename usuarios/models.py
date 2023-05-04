from datetime import datetime
from time import time
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UsuarioManager(BaseUserManager):

    def create_user(self, email, password=None):
        if not email:
            raise ValueError('El usuario debe especificar un correo electrónico.')

        user = self.model(email = self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password=password)
        user.is_admin = True
        user.is_staff = True
        user.tipo_usuario = 'admin'
        user.save()
        return user

class Usuario(AbstractBaseUser):

    username = None
    first_name = None
    last_name = None

    email = models.EmailField('Mail', unique=True, max_length=254, blank=True, null=False)
    is_active = models.BooleanField(default=True)
    tipo_usuario = models.CharField('Tipo de Usuario', max_length=20, blank=False, null=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    objects = UsuarioManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'usuario'
        db_table = 'usuarios'

    def __str__(self):
        return '%s, %s' % (self.email, self.tipo_usuario)

    def has_perm(self, perm, obj = None):
        return True

    def has_module_perms(self, app_label):
        return True
    

class Cliente(models.Model):

    user = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    cliente_id = models.AutoField(primary_key=True)
    
    dni = models.PositiveIntegerField('DNI',unique=True, blank=False, null=False)
    nombre = models.CharField('Nombre', max_length=20, blank=False, null=False)
    apellido = models.CharField('Apellido', max_length=20, blank=False, null=False)
    telefono = models.IntegerField('Telefono', max_length=12, blank=False, null=False)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'cliente'
        db_table = 'clientes'

    def __str__(self) -> str:
        return '%s, %s' % (self.apellido, self.nombre)