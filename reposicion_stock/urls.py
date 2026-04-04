# urlpatterns para la gestión de Solicitudes de Reposición de Stock
from django.urls import path
from . import views

urlpatterns = [
    path("agregar_solicitud/", views.agregar_solicitud_reposicion, name="agregar_solicitud_reposicion"),
    path("listar_solicitud/", views.listar_solicitudes_reposicion, name="listar_solicitudes_reposicion"),
    path("detalle_solicitud/<int:pk>/", views.detalle_solicitud_reposicion, name="detalle_solicitud_reposicion"),
    path("editar_solicitud/<int:pk>/", views.editar_solicitud_reposicion, name="editar_solicitud_reposicion"),
]
