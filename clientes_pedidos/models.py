# clientes_pedidos/models.py

from django.db import models
from django.contrib.auth import get_user_model
from seguridad_usuarios.models import Persona, Empleado




# --------------------------------------------------------------------------
# Modelo para representar a un Cliente
# --------------------------------------------------------------------------
class Cliente(Persona):
    """
    Modelo que representa a un Cliente.
    """

    compras_realizadas = models.PositiveIntegerField(default=0)
    total_gastado = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['nombre', 'razon_social']

    def comprar_vehiculos(self, vehiculos, cantidad=1):
        pass  # Lógica para comprar vehículos

    def __str__(self):
        if self.razon_social:
            return f"{self.razon_social} ({self.ruc})"
        elif self.ruc:
            return f"{self.nombre} {self.apellidos} ({self.ruc})"
        return f"{self.nombre} {self.apellidos} ({self.documento_identidad})"


# --------------------------------------------------------------------------
# Modelo para representar un Pedido
# --------------------------------------------------------------------------
class Pedido(models.Model):
    """
    Modelo que representa un Pedido de un Cliente.
    Puede ser de stock (catálogo) o un pedido a medida (por importar).
    """
    TIPO_PEDIDO = (
        ('stock', 'Pedido de Stock'),
        ('medida', 'Pedido a Medida'),
    )
    ESTADO_PEDIDO = (
        ('pendiente', 'Pendiente de Aprobación'),
        ('aprobado', 'Aprobado'),
        ('rechazado', 'Rechazado'),
        ('en_proceso', 'En Proceso'),
        ('completado', 'Completado'),
        ('cancelado', 'Cancelado'),
    )

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='pedidos')
    vendedor = models.ForeignKey(Empleado, on_delete=models.SET_NULL, null=True, related_name='pedidos_venta')
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADO_PEDIDO, default='pendiente')
    tipo = models.CharField(max_length=10, choices=TIPO_PEDIDO)
    observaciones = models.TextField(blank=True, null=True)
    monto_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    iva = models.DecimalField(max_digits=10, decimal_places=2, default=0)


    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        ordering = ['-fecha_pedido']

    def __str__(self):
        return f"Pedido #{self.pk} - {self.cliente}"

# --------------------------------------------------------------------------
# Modelo para representar un Ítem de Pedido
# --------------------------------------------------------------------------
class ItemPedido(models.Model):
    """
    Modelo que representa un ítem dentro de un Pedido.
    """
    from inventario.models import Vehiculo, Repuesto

    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='items')
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.SET_NULL, null=True, blank=True)
    repuesto = models.ForeignKey(Repuesto, on_delete=models.SET_NULL, null=True, blank=True)
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        self.subtotal = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Ítem de Pedido"
        verbose_name_plural = "Ítems de Pedido"

    def __str__(self):
        if self.vehiculo:
            return f"Ítem de Pedido: {self.vehiculo.nombre} - Cantidad: {self.cantidad}"
        elif self.repuesto:
            return f"Ítem de Pedido: {self.repuesto.nombre} - Cantidad: {self.cantidad}"
        return "Ítem de Pedido sin producto"

# --------------------------------------------------------------------------
# Modelo para representar una Cotización de un Pedido a Medida
# --------------------------------------------------------------------------
class Cotizacion(models.Model):
    """
    Modelo que representa una Cotización para un Pedido a Medida.
    """
    ESTADO_COTIZACION = (
        ('solicitada', 'Solicitada'),
        ('enviada', 'Enviada al Cliente'),
        ('aprobada', 'Aprobada por el Cliente'),
        ('rechazada', 'Rechazada por el Cliente'),
    )
    pedido = models.OneToOneField(Pedido, on_delete=models.SET_NULL, null=True, blank=True, related_name='cotizacion')
    fecha_cotizacion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADO_COTIZACION, default='solicitada')
    descripcion_solicitud = models.TextField(verbose_name="Descripción del Producto Solicitado")
    monto_estimado = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    fecha_validez = models.DateField(verbose_name="Fecha de Validez de la Cotización", null=True, blank=True)

    class Meta:
        verbose_name = "Cotización"
        verbose_name_plural = "Cotizaciones"
        ordering = ['-fecha_cotizacion']

    def __str__(self):
        return f"Cotización #{self.pk} para {self.cliente}"


class ItemCarritoVehiculo(models.Model):
    carrito = models.ForeignKey('Carrito', on_delete=models.CASCADE)
    vehiculo = models.ForeignKey('inventario.Vehiculo', on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.cantidad} x {self.vehiculo}"

class ItemCarritoRepuesto(models.Model):
    carrito = models.ForeignKey('Carrito', on_delete=models.CASCADE)
    repuesto = models.ForeignKey('inventario.Repuesto', on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.cantidad} x {self.repuesto}"

class Carrito(models.Model):
    """
    Modelo que representa un Carrito de Compras para un Cliente.
    """
    cliente = models.OneToOneField(Cliente, on_delete=models.CASCADE, related_name='carrito')
    vehiculos = models.ManyToManyField('inventario.Vehiculo', through='ItemCarritoVehiculo')
    repuestos = models.ManyToManyField('inventario.Repuesto', through='ItemCarritoRepuesto')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    def cancelar_carrito(self):
        self.vehiculos.clear()
        self.repuestos.clear()
        self.save()

    def vaciar_carrito(self):
        self.vehiculos.clear()
        self.repuestos.clear()
        self.save()

    def agregar_vehiculo(self, vehiculo, cantidad=1):
        item, created = ItemCarritoVehiculo.objects.get_or_create(carrito=self, vehiculo=vehiculo)
        if not created:
            item.cantidad += cantidad
        else:
            item.cantidad = cantidad
        item.save()

    def agregar_repuesto(self, repuesto, cantidad=1):
        item, created = ItemCarritoRepuesto.objects.get_or_create(carrito=self, repuesto=repuesto)
        if not created:
            item.cantidad += cantidad
        else:
            item.cantidad = cantidad
        item.save()
    
    def total_items(self):
        total_vehiculos = sum(item.cantidad for item in ItemCarritoVehiculo.objects.filter(carrito=self))
        total_repuestos = sum(item.cantidad for item in ItemCarritoRepuesto.objects.filter(carrito=self))
        return total_vehiculos + total_repuestos
    
    def total_precio(self):
        total_vehiculos = sum(item.cantidad * item.vehiculo.precio for item in ItemCarritoVehiculo.objects.filter(carrito=self))
        total_repuestos = sum(item.cantidad * item.repuesto.precio for item in ItemCarritoRepuesto.objects.filter(carrito=self))
        return total_vehiculos + total_repuestos
    
    def quitar_vehiculo(self, vehiculo):
        ItemCarritoVehiculo.objects.filter(carrito=self, vehiculo=vehiculo).delete()
    
    def quitar_repuesto(self, repuesto):
        ItemCarritoRepuesto.objects.filter(carrito=self, repuesto=repuesto).delete()

    class Meta:
        verbose_name = "Carrito"
        verbose_name_plural = "Carritos"

    def __str__(self):
        return f"Carrito de {self.cliente}"
    
class HistorialCompras(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='historial_compras')
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='historial_compras')
    fecha_compra = models.DateTimeField(auto_now_add=True)
    total_pagado = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Historial de Compra"
        verbose_name_plural = "Historiales de Compras"
        ordering = ['-fecha_compra']

    def __str__(self):
        return f"Compra #{self.pedido.pk} - {self.cliente}"



class ItemCarritoVehiculoVendedor(models.Model):
    carrito = models.ForeignKey('CarritoVendedor', on_delete=models.CASCADE)
    vehiculo = models.ForeignKey('inventario.Vehiculo', on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.cantidad} x {self.vehiculo}"
    
class ItemCarritoRepuestoVendedor(models.Model):
    carrito = models.ForeignKey('CarritoVendedor', on_delete=models.CASCADE)
    repuesto = models.ForeignKey('inventario.Repuesto', on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.cantidad} x {self.repuesto}"
    
    
class CarritoVendedor(models.Model):
    """
    Modelo que representa un Carrito de Compras para un Vendedor.
    """
    vendedor = models.OneToOneField(Empleado, on_delete=models.CASCADE, related_name='carrito_vendedor')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)
    vehiculos = models.ManyToManyField('inventario.Vehiculo', through='ItemCarritoVehiculoVendedor')
    repuestos = models.ManyToManyField('inventario.Repuesto', through='ItemCarritoRepuestoVendedor')
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True, related_name='carritos_vendedor')

    def agregar_cliente(self, cliente):
        self.cliente = cliente
        self.save()
        
    def vaciar_carrito(self):
        self.vehiculos.clear()
        self.repuestos.clear()
        self.save()

    def transferir_a_cliente(self, cliente):
        if hasattr(cliente, 'carrito'):
            cliente.carrito.vaciar_carrito()
            for item in ItemCarritoVehiculoVendedor.objects.filter(carrito=self):
                cliente.carrito.agregar_vehiculo(item.vehiculo, item.cantidad)
            for item in ItemCarritoRepuestoVendedor.objects.filter(carrito=self):
                cliente.carrito.agregar_repuesto(item.repuesto, item.cantidad)
            self.vaciar_carrito()

    def agregar_vehiculo(self, vehiculo, cantidad=1):
        item, created = ItemCarritoVehiculoVendedor.objects.get_or_create(carrito=self, vehiculo=vehiculo)
        if not created:
            item.cantidad += cantidad
        else:
            item.cantidad = cantidad
        item.save()

    def agregar_repuesto(self, repuesto, cantidad=1):
        item, created = ItemCarritoRepuestoVendedor.objects.get_or_create(carrito=self, repuesto=repuesto)
        if not created:
            item.cantidad += cantidad
        else:
            item.cantidad = cantidad
        item.save()
    
    def total_items(self):
        total_vehiculos = sum(item.cantidad for item in ItemCarritoVehiculoVendedor.objects.filter(carrito=self))
        total_repuestos = sum(item.cantidad for item in ItemCarritoRepuestoVendedor.objects.filter(carrito=self))
        return total_vehiculos + total_repuestos
    
    def total_precio(self):
        total_vehiculos = sum(item.cantidad * item.vehiculo.precio for item in ItemCarritoVehiculoVendedor.objects.filter(carrito=self))
        total_repuestos = sum(item.cantidad * item.repuesto.precio for item in ItemCarritoRepuestoVendedor.objects.filter(carrito=self))
        return total_vehiculos + total_repuestos
    
    def quitar_vehiculo(self, vehiculo):
        ItemCarritoVehiculoVendedor.objects.filter(carrito=self, vehiculo=vehiculo).delete()
    
    def quitar_repuesto(self, repuesto):
        ItemCarritoRepuestoVendedor.objects.filter(carrito=self, repuesto=repuesto).delete()

    class Meta:
        verbose_name = "Carrito del Vendedor"
        verbose_name_plural = "Carritos de los Vendedores"