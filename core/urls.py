from django.urls import path
from . import views
from .views import ConvertCurrencyView

app_name = "CORE"

urlpatterns = [
    # PRODUCTOS
    path('', views.producto_index, name="producto_index"), #PAGINA PRINCIPAL
    path('producto/agregar', views.producto_create, name="producto_create" ),
    path('producto/<int:producto_id>', views.producto_show, name="producto_show" ),
    path('producto/<int:producto_id>/editar', views.producto_edit, name="producto_edit" ),
    path('producto/<int:producto_id>/eliminar', views.producto_delete, name="producto_delete" ),
    path('producto/buscador', views.producto_search, name="producto_search"),
    path('categoria/<int:categoria_id>/productos', views.productos_por_categoria, name="productos_por_categoria"),

    # REGISTRAR USUARIO
    path('registrarse/', views.register, name="register"),

    # CARRITO
    path('carrito/', views.carrito_index, name="carrito_index"),
    path('carrito/agregar', views.carrito_save, name="carrito_save"),
    path('carrito/clean', views.carrito_clean, name="carrito_clean"),
    path('item_carrito/<int:item_carrito_id>/eliminar', views.item_carrito_delete, name="item_carrito_delete"),

    path('convert_currency/', ConvertCurrencyView.as_view(), name='convert_currency'),
]