from django.core.management.base import BaseCommand
from inventario.models import UnidadMedida

class Command(BaseCommand):
    help = 'Carga unidades de medida iniciales en la base de datos'

    def handle(self, *args, **kwargs):
        unidades_medida_iniciales = [
            {'nombre': 'Kilogramo', 'abreviatura': 'kg'},
            {'nombre': 'Litro', 'abreviatura': 'l'},
            {'nombre': 'Metro', 'abreviatura': 'm'},
            {'nombre': 'Unidad', 'abreviatura': 'u'},
            {'nombre': 'Caja', 'abreviatura': 'caja'},
            {'nombre': 'Paquete', 'abreviatura': 'paq'},
            {'nombre': 'Gramo', 'abreviatura': 'g'},
            {'nombre': 'Mililitro', 'abreviatura': 'ml'},
            {'nombre': 'Centímetro', 'abreviatura': 'cm'},
            {'nombre': 'Pieza', 'abreviatura': 'pz'},
            {'nombre': 'Tonelada', 'abreviatura': 't'},
        ]
        
        for unidad in unidades_medida_iniciales:
            UnidadMedida.objects.get_or_create(
                nombre=unidad['nombre'],
                defaults={'abreviatura': unidad['abreviatura']}
            )
        
        self.stdout.write(self.style.SUCCESS('Unidades de medida cargadas correctamente.'))
