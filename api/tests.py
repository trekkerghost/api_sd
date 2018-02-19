'''Definición de pruebas'''
from django.test import TestCase
from django.urls import reverse

from api.models import Product, ProductTags


class ModelTestCase(TestCase):
    '''Clase para las pruebas de los modelos'''

    def setUp(self):
        '''Definir un producto'''
        self.name = "Prueba de creación de productos"
        self.tags = ProductTags(name='nuevo')
        self.producto = Product(
            name='Producto 1',
            description='Producto de prueba 1',
            quantity=20.5)

    def test_modelo_puede_crear_producto(self):
        '''Prueba la creacion del modelo producto'''
        cantidad_productos_antes = Product.objects.count()
        self.producto.save()
        self.tags.save()
        self.producto.tags.add(self.tags)
        self.producto.save()
        cantidad_productos_despues = Product.objects.count()
        self.assertNotEqual(cantidad_productos_antes,
                            cantidad_productos_despues)
