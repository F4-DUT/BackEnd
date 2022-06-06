from rest_framework import serializers

from api_product.models import Product, ProductImage


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['category'] = instance.category.name
        product_image = ProductImage.objects.filter(product_id=instance.id).first()
        if product_image:
            ret['image'] = product_image.image
        else:
            ret['image'] = None
        return ret


