from django.db import models

class Sucursal(models.Model):
    nombre = models.CharField(max_length=255)
    ubicacion = models.TextField()
    telefono = models.CharField(max_length=15)

    def __str__(self):
        return self.nombre

class InventarioSucursal(models.Model):
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)
    producto = models.ForeignKey('ventas.Producto', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.producto.nombre} en {self.sucursal.nombre}"
