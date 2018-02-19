'''Definicion de vistas de la API'''
from django.conf.urls import url

from api.views import APIProductos

urlpatterns = [
    url(r'^list/$', APIProductos.as_view(), name='list'),
    url(r'^create/$', APIProductos.as_view(), name='create'),
    url(r'^get/(?P<pk>[0-9]+)/$', APIProductos.as_view(), name='get'),
    url(r'^update/(?P<pk>[0-9]+)/$', APIProductos.as_view(), name='update'),
    url(r'^delete/(?P<pk>[0-9]+)/$', APIProductos.as_view(), name='delete'),
]
