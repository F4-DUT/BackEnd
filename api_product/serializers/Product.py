from rest_framework import serializers

from api_product.models import Product


class ProductSerializer(serializers.ModelSerializer):
    model = Product
    fields = '__all__'
