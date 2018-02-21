from api.models import Product, ProductDetail
from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('name', 'description', 'tags', 'created_at', 'is_active',
                  'product_type', 'is_variation', 'brand', 'code', 'family',
                  'is_complement', 'is_delete')
