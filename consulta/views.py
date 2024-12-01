from django.shortcuts import render, get_object_or_404
from .models import Sucursal

def lista_sucursales(request):
    sucursales = Sucursal.objects.all()
    return render(request, 'index.html', {'sucursales' : sucursales})

def productos_en_sucursal(request, sucursal):
    sucursalId = get_object_or_404(Sucursal, pk=sucursal)
    return render(request, 'inventario_suc.html', {'sucursalId': sucursalId})