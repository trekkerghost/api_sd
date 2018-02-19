'''Definicion de vistas de la API'''
from django.http import JsonResponse
from django.views import View
from django.db.models import ObjectDoesNotExist

from api.models import Product, ProductTags

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

    def post(self, request, *args, **kwargs):
        post_data = request.POST.copy()

        if post_data:
            tags = [ProductTags(name=tag) for tag in post_data.get('tags')]
            producto = Product(
                name=post_data.get('name'),
                description=post_data.get('description'),
                quantity=post_data.get('quantity'))
            try:
                producto.save()
                producto.tags.add(tags)
                producto.save()
                return JsonResponse(
                    {
                        'response': 'Producto creado satisfactoriamente',
                        'id': producto.pk
                    },
                    safe=False)
            except Exception:
                return JsonResponse(
                    {
                        'response': 'Error al crear el producto'
                    }, safe=False)
        else:
            return JsonResponse(
                {
                    'response': 'Petición incorrecta'
                }, safe=False)
