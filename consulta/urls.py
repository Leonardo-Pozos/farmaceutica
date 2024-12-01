from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = "consulta"
urlpatterns = [
    path('', views.lista_sucursales, name='lista_sucursales'),
    path('sucursal/<int:sucursal>/', views.productos_en_sucursal, name='productos_en_sucursal'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login')
]