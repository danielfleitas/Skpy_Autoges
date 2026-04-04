from django.core.management.base import BaseCommand
from seguridad_usuarios.models import Permiso
from clientes_pedidos.views import permisos_iniciales_clientes_pedidos
from configuraciones_maestras.views import permisos_iniciales_configuraciones_maestras
from seguridad_usuarios.views import permisos_iniciales_seguridad_usuarios
from inventario.views import permisos_iniciales_inventario
#from reposicion_stock.views import permisos_iniciales_reposicion_stock


class Command(BaseCommand):
    help = 'Carga permisos iniciales en la base de datos'

    def handle(self, *args, **kwargs):
        permisos_iniciales = buscar_permisos()
        for permiso in permisos_iniciales:
            Permiso.objects.get_or_create(
                codename=permiso['codename'],
                defaults={
                    'nombre': permiso['nombre'],
                    'descripcion': permiso['descripcion']
                }
            )
        self.stdout.write(self.style.SUCCESS('Permisos cargados correctamente.'))

def buscar_permisos():
    """Función para buscar y combinar permisos iniciales de diferentes módulos."""
    permisos = []
    permisos.extend(permisos_iniciales_clientes_pedidos)
    permisos.extend(permisos_iniciales_configuraciones_maestras)
    permisos.extend(permisos_iniciales_seguridad_usuarios)
    permisos.extend(permisos_iniciales_inventario)
    #permisos.extend(permisos_iniciales_reposicion_stock)
    return permisos