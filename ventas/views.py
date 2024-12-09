from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto, Venta
from consulta.models import Sucursal, InventarioSucursal
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError

@login_required
def lista_productos(request, idSucursal=None):
    sucursales = Sucursal.objects.all()
    sucursal_seleccionada = None
    productos = []
    if idSucursal:
        sucursal_seleccionada = get_object_or_404(Sucursal, id=idSucursal)
        inventario = InventarioSucursal.objects.filter(sucursal=sucursal_seleccionada)
        productos = [item.producto for item in inventario]
    return render(request, 'lista_productos.html', { 'productos': productos, 'sucursales': sucursales, 'sucursal_seleccionada': sucursal_seleccionada})


@login_required
def agregar_producto(request):
    sucursales = Sucursal.objects.all()
    error = None
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        precio = request.POST.get('precio')
        descripcion = request.POST.get('descripcion')
        stock = request.POST.get('stock')
        sucursal_id = request.POST.get('sucursal')
        try:
            if not nombre or not precio or not descripcion or not stock or not sucursal_id:
                raise ValueError("Todos los campos son obligatorios.")
            inventario_existente = InventarioSucursal.objects.filter(sucursal=sucursal_id,producto__nombre=nombre).exists()
            if inventario_existente:
                raise IntegrityError(f"El producto '{nombre}' ya existe en el inventario de la sucursal seleccionada.")
            producto = Producto.objects.create(nombre=nombre, precio=precio, descripcion=descripcion, stock=stock)
            sucursal = Sucursal.objects.get(id=sucursal_id)
            InventarioSucursal.objects.create(sucursal = sucursal, producto = producto)
            return redirect('ventas:agregar_producto')
        except (ValueError, IntegrityError) as e:
            error = str(e)
    return render(request, 'inventario.html', {'error': error, 'sucursales': sucursales})


@login_required
def venta_productos(request, idSucursal=None):
    sucursales = Sucursal.objects.all()
    error = None
    productos = None
    ventas = Venta.objects.filter(sucursal__id=idSucursal).order_by('-fecha')[:10] if idSucursal else []
    sucursal_seleccionada = None 
    productos_seleccionados = None
    venta_realizada = []
    costo_total = 0

    if idSucursal:
        sucursal_seleccionada = get_object_or_404(Sucursal, id=idSucursal)
    if sucursal_seleccionada:
        inventario = InventarioSucursal.objects.filter(sucursal=sucursal_seleccionada)
        productos = [item.producto for item in inventario]

    if request.method == "POST":
        try:
            if 'confirmar_venta' in request.POST:
                productos_seleccionados = False
                for item in inventario:
                    producto = item.producto
                    cantidad_key = f'cantidad_{producto.id}'
                    cantidad = request.POST.get(cantidad_key)
                    
                    if not cantidad:
                        continue
                    
                    productos_seleccionados = True
                    cantidad = int(cantidad)
                    
                    if producto.stock < cantidad:
                        raise ValueError(f"No hay suficiente stock para '{producto.nombre}'. Disponible: {producto.stock}.")
                    
                    # Calcular el total del producto
                    total_producto = producto.precio * cantidad
                    
                    # Actualizar stock y guardar venta
                    producto.stock -= cantidad
                    producto.save()

                    venta_re = Venta.objects.create(
                        producto=producto,
                        cantidad=cantidad,
                        precio_total=total_producto,
                        sucursal=sucursal_seleccionada
                    )

                    venta_realizada.append(venta_re)
                    costo_total += total_producto
                
                if not productos_seleccionados:
                    raise ValueError("Debe seleccionar al menos un producto e indicar la cantidad para realizar una venta.")
                
                return render(request, 'ventas.html', {
                    'error': error,
                    'productos': productos,
                    'ventas': ventas,
                    'sucursales': sucursales,
                    'sucursal_seleccionada': sucursal_seleccionada,
                    'costo_total': costo_total,
                    'venta_realizada': venta_realizada
                })
        except (ValueError, Sucursal.DoesNotExist) as e:
            error = str(e)
            
    return render(request, 'ventas.html', {
        'error': error,
        'productos': productos,
        'ventas': ventas,
        'sucursales': sucursales,
        'sucursal_seleccionada': sucursal_seleccionada
    })

@login_required
def incrementar_stock(request, producto_id, idSucursal=None):
    producto = get_object_or_404(Producto, id=producto_id)
    producto.stock += 1
    producto.save()
    return redirect('ventas:lista_productos', idSucursal=idSucursal)

@login_required
def disminuir_stock(request, producto_id, idSucursal=None):
    producto = get_object_or_404(Producto, id=producto_id)
    if producto.stock > 0:
        producto.stock -= 1
        producto.save()
    return redirect('ventas:lista_productos', idSucursal=idSucursal)