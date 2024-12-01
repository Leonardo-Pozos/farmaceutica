from django.shortcuts import render
from .models import Producto
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def lista_productos(request):
    # query = request.GET.get('q', '')

    # if query:
    #     productos = Producto.objects.filter(nombre__icontains=query)
    # else:
    productos = Producto.objects.all()
    return render(request, 'lista_productos.html', {'productos': productos})