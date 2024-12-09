from django.test import TestCase
from django.contrib.auth.models import User
from .models import Producto
from .models import Venta

class ProductoTestCase(TestCase):
    def setUp(self):
        # Crear un producto de ejemplo
        self.producto = Producto.objects.create(
            nombre="Aspirina",
            descripcion="Medicamento para el dolor de cabeza",
            precio=50.00,
            stock=100
        )
    def test_producto_str(self):
        # Verificar que el método __str__ devuelve el nombre correctamente
        self.assertEqual(str(self.producto), "Aspirina")
    
    def test_producto_guardado_correctamente(self):
        # Comprobar que los datos del producto se guardaron correctamente
        self.assertEqual(self.producto.descripcion, "Medicamento para el dolor de cabeza")
        self.assertEqual(self.producto.precio, 50.00)
        self.assertEqual(self.producto.stock, 100)

    def test_precio_positivo(self):
        # Verificar que el precio del producto es positivo
        self.assertGreater(self.producto.precio, 0)

class VentaTestCase(TestCase):
    def setUp(self):
        self.producto = Producto.objects.create(
            nombre="Paracetamol",
            descripcion="muy buena",
            precio=199.00,
            stock=2
        )
        self.venta = Venta.objects.create(
            producto=self.producto,
            cantidad=2,
            precio_total=398.00
        )

    def test_venta_str(self):
        #verificar que el método __str__ del modelo Venta devolviendo producto, cantidad, precio
        self.assertEqual(
            str(self.venta),
            "Paracetamol - 2 unidades - $398.00"
        )

    def test_venta_guardada_correctamente(self):
        # Comprobar que los datos de la venta se guardaron correctamente
        self.assertEqual(self.venta.producto.nombre, "Paracetamol")
        self.assertEqual(self.venta.cantidad, 2)
        self.assertEqual(self.venta.precio_total, 398.00)
    
    def test_stock_reducido_correctamente(self):
        # Simular la reducción del stock tras una venta
        stock_inicial = self.producto.stock
        self.producto.stock -= self.venta.cantidad
        self.producto.save()
        self.assertEqual(self.producto.stock, stock_inicial - self.venta.cantidad)