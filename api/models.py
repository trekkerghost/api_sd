''' Declaración de modelos usados por la API'''
from django.db import models
from django.utils.translation import ugettext_lazy as _


class ProductTags(models.Model):
    '''Definición de modelo para etiquetas del producto'''
    name = models.CharField(
        max_length=220, blank=False, null=False, verbose_name=_('Tag Name'))

    def __str__(self):
        return self.name


class Brand(models.Model):
    '''Definición de modelo para marca del producto'''
    name = models.CharField(
        max_length=220, blank=False, null=False, verbose_name=_('Brand Name'))

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
    tags = models.ManyToManyField(
        ProductTags, blank=True, verbose_name=_('Product tags'))
    created_at = models.DateTimeField(
        auto_now_add=True, editable=False, verbose_name=_('Creation date'))
    updated_at = models.DateTimeField(
        auto_now=True, editable=False, verbose_name=_('Modified date'))
    is_active = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    product_type = models.CharField(max_length=2, blank=True, null=True)
    is_variation = models.BooleanField(default=False)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    code = models.IntegerField(default=0)
    family = models.IntegerField(default=0)
    is_complement = models.BooleanField(default=False)
    is_delete = models.BooleanField(default=False)

    def __str__(self):
        return "Producto ['id':{0}, 'name':{1}]".format(self.pk, self.name)


class ProductDetail(models.Model):
    created = models.DateTimeField(
        editable=False, verbose_name=_('Creation date'))
    modified = models.DateTimeField(
        editable=False, verbose_name=_('Modified date'))
    is_active = models.BooleanField(default=False, verbose_name=_('Activo'))
    is_visibility = models.BooleanField(
        default=False, verbose_name=_('Visible'))
    price = models.DecimalField(
        decimal_places=3,
        max_digits=10,
        default=False,
        verbose_name=_('Precio'))
    price_offer = models.DecimalField(
        decimal_places=3,
        max_digits=10,
        default=False,
        blank=True,
        null=True,
        verbose_name=_('Precio de  Oferta'))
    offer_day_from = models.DateTimeField(
        blank=True, null=True, verbose_name=_('Fecha de inicio de oferta'))
    offer_day_to = models.DateTimeField(
        blank=True, null=True, verbose_name=_('Fecha de fin de oferta'))
    sku = models.IntegerField(default=0, verbose_name=_('SKU'))
    quantity = models.DecimalField(
        blank=False,
        null=False,
        decimal_places=3,
        max_digits=10,
        verbose_name=_('Product quantity'))
    product = models.OneToOneField(Product)
