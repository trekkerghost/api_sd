'''Definicion de vistas de la API'''
import math

from django.db.models import ObjectDoesNotExist
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import UpdateModelMixin
from rest_framework.response import Response

from api.models import Product, ProductTags
from api.serializers import ProductSerializer


def format_product(producto):
    '''retorna un producto como un diccionario'''
    return {
        'id': producto.pk,
        'name': producto.description,
        'tags': [{
            'id': tag.id,
            'name': tag.name
        } for tag in producto.tags.all()],
        'created_at': producto.created_at,
        'updated_at': producto.updated_at,
        'is_active': producto.is_active,
        'product_type': producto.product_type,
        'is_variation': producto.is_variation,
        'brand': {
            'brand_id': producto.brand.pk,
            'brand_name': producto.brand.name
        },
        'code': producto.code,
        'family': producto.family,
        'is_complement': producto.is_complement,
        'is_delete': producto.is_delete,
        'detalle': {
            'created': producto.productdetail.created,
            'modified': producto.productdetail.modified,
            'is_active': producto.productdetail.is_active,
            'is_visibility': producto.productdetail.is_visibility,
            'price': producto.productdetail.price,
            'price_offer': producto.productdetail.price_offer,
            'offer_day_from': producto.productdetail.offer_day_from,
            'offer_day_to': producto.productdetail.offer_day_to,
            'sku': producto.productdetail.sku,
            'quantity': producto.productdetail.quantity,
        }
    }


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
                producto = Product.objects.prefetch_related(
                    'tags').select_related(
                        'brand', 'productdetail').get(pk=id_producto)
                return JsonResponse(format_product(producto), safe=False)
            except ObjectDoesNotExist:
                return JsonResponse({'response': 'Producto no encontrado'})
        else:
            # queremos la lista
            total_registros = Product.objects.count()
            if total_registros:
                ### datos para paginacion
                pagina = int(request.GET.get('page', 1))
                limite = int(request.GET.get('limite', 10))
                numero_paginas = math.ceil(total_registros / limite)
                offset = (pagina - 1) * limite
                lista_productos = [
                    format_product(producto)
                    for producto in Product.objects.prefetch_related('tags')
                    .select_related('brand', 'productdetail').all()[offset:
                                                                    limite]
                ]
                data = {
                    'productos': lista_productos,
                    'links_pagination': {
                        "self": {
                            "href":
                            request.build_absolute_uri(
                                '/api/list/?page={0}&limite={1}'.format(
                                    pagina, limite))
                        },
                        "first": {
                            "href": request.build_absolute_uri('/api/list/')
                        },
                        "prev": {
                            "href":
                            request.build_absolute_uri(
                                '/api/list/?page={0}&limite={1}'.format(
                                    pagina - 1, limite)) if pagina - 1 else
                            request.build_absolute_uri('/api/list/')
                        },
                        "next": {
                            "href":
                            request.build_absolute_uri(
                                '/api/list/?page={0}&limite={1}'.format(
                                    pagina + 1, limite))
                            if pagina + 1 <= numero_paginas
                            else request.build_absolute_uri(
                                '/api/list/?page={0}'.format(numero_paginas))
                        },
                        "last": {
                            "href":
                            request.build_absolute_uri(
                                '/api/list/?page={0}'.format(numero_paginas))
                        }
                    }
                }
                return JsonResponse(data, safe=False)
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
            producto = Product(name=nombre, description=descripcion)
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


class ProductPartialUpdateView(GenericAPIView, UpdateModelMixin):
    '''
    Definición de metodo PATCH
    '''
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
