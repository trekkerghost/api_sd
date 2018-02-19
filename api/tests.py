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


class APITestCase(TestCase):
    '''Definición de las pruebas para la vista de la API'''

    def setUp(self):
        pass

    def test_no_hay_productos(self):
        response = self.client.get(reverse('api:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No existen productos')

    def test_producto_no_existe(self):
        response = self.client.get(reverse('api:get', kwargs={'pk': 0}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Producto no encontrado')

    def test_borrar_producto(self):
        self.tags = ProductTags(name='nuevo')
        self.producto = Product(
            name='Producto 1',
            description='Producto de prueba 1',
            quantity=20.5)
        self.producto.save()
        self.tags.save()
        self.producto.tags.add(self.tags)
        self.producto.save()
        print(self.producto)
        response = self.client.delete(
            reverse('api:delete', kwargs={
                'pk': self.producto.pk
            }))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Se ha eliminado satisfactoriamente')
