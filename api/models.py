''' Declaración de modelos usados por la API'''
import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _


class ProductTags(models.Model):
    '''Definición de modelo para etiquetas del producto'''
    name = models.CharField(
        max_length=220, blank=False, null=False, verbose_name=_('Tag Name'))

    def __str__(self):
        return self.name


class Product(models.Model):
    '''Definición de modelo Producto'''
    name = models.CharField(
        max_length=220,
        blank=False,
        null=False,
        verbose_name=_('Product Name'))
    description = models.TextField(
        blank=False, null=False, verbose_name=_('Product Description'))
    quantity = models.DecimalField(
        blank=False,
        null=False,
        decimal_places=3,
        max_digits=10,
        verbose_name=_('Product quantity'))
    tags = models.ManyToManyField(ProductTags, blank=True, verbose_name=_('Product tags'))
    created_at = models.DateTimeField(
        auto_now_add=True,  editable=False, verbose_name=_('Creation date'))
    updated_at = models.DateTimeField(
        auto_now=True,
        editable=False,
        verbose_name=_('Modified date'))

    def __str__(self):
        return "Producto ['id':{0}, 'name':{1}]".format(self.pk, self.name )
