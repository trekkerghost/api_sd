'''Definicion de vistas de la API'''
from django.http import JsonResponse
from django.views import View
from django.db.models import ObjectDoesNotExist

from api.models import Product

# Create your views here.


class APIProductos(View):
    def get(self, *args, **kwargs):
        '''Definición de método GET para listar y obtener'''
        if 'pk' in kwargs:
        #Si existe un parámetro en la URL estamos buscando un producto
            try:
                id_producto = kwargs.get('id', None)
                producto = Product.objects.prefetch_related('tags').get(
                    pk=id_producto)
                return JsonResponse(
                    {
                        'id':
                        producto.pk,
                        'name':
                        producto.description,
                        'quantity':
                        producto.quantity,
                        'tags': [{
                            'id': tag.id,
                            'name': tag.name
                        } for tag in producto.tag.all()]
                    },
                    safe=False)
            except ObjectDoesNotExist:
                return JsonResponse({'response': 'Producto no encontrado'})
        else:
            lista_productos = [{
                'id':
                producto.pk,
                'name':
                producto.description,
                'quantity':
                producto.quantity,
                'tags': [{
                    'id': tag.id,
                    'name': tag.name
                } for tag in producto.tag.all()]
            } for producto in Product.objects.prefetch_related('tags').all()]
            if lista_productos:
                return JsonResponse(lista_productos, safe=False)
            else:
                return JsonResponse({'response': 'No existen productos'})
