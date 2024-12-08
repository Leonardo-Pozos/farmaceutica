from django.test import TestCase
from ventas.models import Producto  
from .models import Sucursal, InventarioSucursal

class SucursalModelTest(TestCase):

    def setUp(self):
        self.sucursal = Sucursal.objects.create(
            nombre="Sucursal Central",
            ubicacion="Calle Principal #123, Ciudad",
            telefono="1234567890"
        )

    def test_crear_sucursal(self):
        """Prueba que se puede crear una sucursal correctamente."""
        self.assertEqual(Sucursal.objects.count(), 1)
        self.assertEqual(self.sucursal.nombre, "Sucursal Central")
        self.assertEqual(self.sucursal.telefono, "1234567890")

    def test_actualizar_sucursal(self):
        """Prueba que se puede actualizar una sucursal."""
        self.sucursal.nombre = "Sucursal Actualizada"
        self.sucursal.save()
        self.assertEqual(self.sucursal.nombre, "Sucursal Actualizada")

    def test_eliminar_sucursal(self):
        """Prueba que se puede eliminar una sucursal."""
        self.sucursal.delete()
        self.assertEqual(Sucursal.objects.count(), 0)


class InventarioSucursalModelTest(TestCase):

    def setUp(self):
        self.sucursal = Sucursal.objects.create(
            nombre="Sucursal Central",
            ubicacion="Calle Principal #123, Ciudad",
            telefono="1234567890"
        )
        self.producto = Producto.objects.create(
            nombre="Producto Prueba",
            descripcion="Descripción de prueba",
            precio=100.0
        )
        self.inventario = InventarioSucursal.objects.create(
            sucursal=self.sucursal,
            producto=self.producto
        )

    def test_crear_inventario(self):
        """Prueba que se puede crear un inventario correctamente."""
        self.assertEqual(InventarioSucursal.objects.count(), 1)
        self.assertEqual(self.inventario.sucursal, self.sucursal)
        self.assertEqual(self.inventario.producto, self.producto)

    def test_relacion_sucursal_producto(self):
        """Prueba que la relación entre sucursal y producto funciona correctamente."""
        self.assertEqual(self.inventario.sucursal.nombre, "Sucursal Central")
        self.assertEqual(self.inventario.producto.nombre, "Producto Prueba")

    def test_eliminar_inventario(self):
        """Prueba que se puede eliminar un inventario."""
        self.inventario.delete()
        self.assertEqual(InventarioSucursal.objects.count(), 0)