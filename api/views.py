'''Definicion de vistas de la API'''
from django.db.models import ObjectDoesNotExist
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from api.models import Product, ProductTags

# Create your views here.

@method_decorator(csrf_exempt, name='dispatch')
#para pruebas
class APIProductos(View):
    '''Definición de la API'''
    def get(self, request, *args, **kwargs):
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
        ''' Implementación del método POST'''
        post_data = request.POST.copy()
        if post_data:
            tags = [ProductTags(name=tag) for tag in post_data.getlist('tags')]
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

    def delete(self, request, *args, **kwargs):
        '''Definición de método DELETE para eliminar'''
        if 'pk' in kwargs:
            #Si existe un parámetro en la URL estamos buscando un producto
            try:
                id_producto = kwargs.get('pk', None)
                Product.objects.prefetch_related('tags').get(
                    pk=id_producto).delete()
                return JsonResponse(
                    {
                        'response': 'Se ha eliminado satisfactoriamente'
                    },
                    safe=False)
            except ObjectDoesNotExist:
                return JsonResponse({'response': 'Producto no encontrado'})
