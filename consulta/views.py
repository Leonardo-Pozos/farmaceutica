from django.shortcuts import render, get_object_or_404
from .models import Sucursal, InventarioSucursal

def lista_sucursales(request):
    sucursales = Sucursal.objects.all()
    return render(request, 'index.html', {'sucursales' : sucursales})

def productos_en_sucursal(request, sucursal):
    sucursalId = get_object_or_404(Sucursal, pk=sucursal)
    inventario = InventarioSucursal.objects.filter(sucursal = sucursal)
    productos = [item.producto for item in inventario]
    return render(request, 'inventario_suc.html', {'sucursalId': sucursalId, 'productos': productos})