from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto, Venta
from django.contrib.auth.decorators import login_required
from .forms import ProductoForm, VentaForm
from django.contrib import messages
from django.db import IntegrityError

@login_required
def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'lista_productos.html', {'productos': productos})

@login_required
def agregar_producto(request):
    error = None
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        precio = request.POST.get('precio')
        descripcion = request.POST.get('descripcion')
        stock = request.POST.get('stock')
        try:
            if not nombre or not precio or not descripcion or not stock:
                raise ValueError("Todos los campos son obligatorios.")

            if Producto.objects.filter(nombre=nombre).exists():
                raise IntegrityError("Ya existe un producto con este nombre.")

            Producto.objects.create(
                nombre=nombre,
                precio=precio,
                descripcion=descripcion,
                stock=stock
            )
            return redirect('ventas:agregar_producto')
        except (ValueError, IntegrityError) as e:
            error = str(e)
    productos = Producto.objects.all()
    return render(request, 'inventario.html', {'error': error, 'productos': productos})


@login_required
def venta_productos(request):
    error = None
    if request.method == "POST":
        try:
            productos_seleccionados = False
            for producto in Producto.objects.all():
                cantidad_key = f'cantidad_{producto.id}'
                cantidad = request.POST.get(cantidad_key)
                if not cantidad:
                    continue  
                productos_seleccionados = True
                cantidad = int(cantidad)
                if producto.stock < cantidad:
                    raise ValueError(f"No hay suficiente stock para {producto.nombre}. Disponible: {producto.stock}.")
                producto.stock -= cantidad
                producto.save()
                Venta.objects.create(producto=producto, cantidad=cantidad, usuario=request.user)
            if not productos_seleccionados:
                raise ValueError("Debe seleccionar al menos un producto e indicar la cantidad para realizar una venta.")    
            return redirect('ventas:venta_productos')
        except ValueError as e:
            error = str(e)
    productos = Producto.objects.all()
    ventas = Venta.objects.all().order_by('-fecha')[:10]
    return render(request, 'ventas.html', {'error': error, 'productos': productos, 'ventas': ventas})


def incrementar_stock(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    producto.stock += 1
    producto.save()
    return redirect('ventas:lista_productos')

def disminuir_stock(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if producto.stock > 0:
        producto.stock -= 1
        producto.save()
    return redirect('ventas:lista_productos')