from django.contrib.auth.management.commands.createsuperuser import Command as BaseCommand
from django.core.management.base import CommandError
from django.core.exceptions import ValidationError


class Command(BaseCommand):
    help = 'Crea un superusuario'

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument('--dni', type=int, help='El DNI del usuario')
        parser.add_argument('--nombre', type=str, help='El nombre del usuario')
        parser.add_argument('--apellido', type=str, help='El apellido del usuario')
        parser.add_argument('--telefono', type=int, help='El telefono del usuario')

    def handle(self, *args, **options):
        email = options.get('email')
        password = options.get('password')
        dni = options.get('dni')
        nombre = options.get('nombre')
        apellido = options.get('apellido')
        telefono = options.get('telefono')

        if not email:
            email = input('Correo electronico: ')
        if not password:
            password = input('Contraseña: ')
        if not dni:
            dni = input('DNI: ')
        if not nombre:
            nombre = input('Nombre: ')
        if not apellido:
            apellido = input('Apellido: ')
        if not telefono:
            telefono = input('Telefono: ')

        try:
            self.UserModel._default_manager.db_manager('default').create_superuser(
                email=email,
                password=password,
                dni=dni,
                nombre=nombre,
                apellido=apellido,
                telefono=telefono
            )
        except ValidationError as e:
            raise CommandError('; '.join(e.messages))

        self.stdout.write('Superusuario creado satisfactoriamente.')