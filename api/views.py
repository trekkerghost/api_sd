'''Definicion de vistas de la API'''
import json

from django.db.models import ObjectDoesNotExist
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.models import Product, ProductTags
from api.serializers import ProductSerializer


#para pruebas
@method_decorator(csrf_exempt, name='dispatch')
class APIProductos(View):
    '''Definición de la API'''

    def get(self, request, *args, **kwargs):
        '''Definición de método GET para listar y obtener'''
        if 'pk' in kwargs:
            #Si existe un parámetro en la URL estamos buscando un producto
            try:
                id_producto = kwargs.get('pk', None)
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
                        } for tag in producto.tags.all()]
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
                } for tag in producto.tags.all()]
            } for producto in Product.objects.prefetch_related('tags').all()]
            if lista_productos:
                return JsonResponse(lista_productos, safe=False)
            else:
                return JsonResponse({'response': 'No existen productos'})

    def post(self, request, *args, **kwargs):
        ''' Implementación del método POST'''
        post_data = dict(request.POST)
        if post_data:
            lista_tags = []
            for tag in post_data.get('tags')[0].split(','):
                nueva_tag = ProductTags(name=tag)
                nueva_tag.save()
                lista_tags.append(nueva_tag)
            nombre = post_data.get('name')[0]
            descripcion = post_data.get('description')[0]
            cantidad = post_data.get('quantity')[0]
            producto = Product(
                name=nombre, description=descripcion, quantity=cantidad)
            try:
                producto.save()
                for tag in lista_tags:
                    producto.tags.add(tag)
                producto.save()
                return JsonResponse(
                    {
                        'response': 'Producto creado satisfactoriamente',
                        'id': producto.pk
                    },
                    safe=False)
            except Exception as e:
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


@api_view(['PUT'])
def actualizar(request, pk):
    '''Definición de método PUT para actualizar'''
    try:
        producto = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = ProductSerializer(producto, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            data = serializer.data
            data['reponse'] = 'Producto modificado satisfactoriamente'
            return Response(data)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)
