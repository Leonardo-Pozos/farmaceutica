from django.urls import path
from . import views

app_name = "ventas"
urlpatterns = [
    path('', views.lista_productos, {'idSucursal': 0}, name='lista_productos'),
    path('<int:idSucursal>/', views.lista_productos, name='lista_productos'),
    path('agregar_producto', views.agregar_producto, name="agregar_producto"),
    path('vender_productos/', views.venta_productos, {'idSucursal': 0}, name='venta_productos'),
    path('vender_productos/<int:idSucursal>/', views.venta_productos, name='venta_productos'),
    path('incrementar_stock/<int:producto_id>/<int:idSucursal>/', views.incrementar_stock, name='incrementar_stock'),
    path('disminuir_stock/<int:producto_id>/<int:idSucursal>/', views.disminuir_stock, name='disminuir_stock')
]