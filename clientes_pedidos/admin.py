# clientes_pedidos/admin.py
from django.contrib import admin
from .models import Cliente, Pedido, ItemPedido, Cotizacion, Carrito, ItemCarritoRepuesto 
from .models import ItemCarritoVehiculo, ItemCarritoVehiculoVendedor, ItemCarritoRepuestoVendedor, CarritoVendedor

admin.site.register(Cliente)
admin.site.register(Pedido)
admin.site.register(ItemPedido)
admin.site.register(Cotizacion)
admin.site.register(Carrito)
admin.site.register(ItemCarritoRepuesto)
admin.site.register(ItemCarritoVehiculo)
admin.site.register(ItemCarritoVehiculoVendedor)
admin.site.register(ItemCarritoRepuestoVendedor)
admin.site.register(CarritoVendedor)

