from django.db import models

from api_base.models import TimeStampedModel
from api_product.models import Product


class ProductImage(TimeStampedModel):
    image = models.CharField(max_length=255, null=True, blank=True)

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")

    class Meta:
        db_table = 'product_image'
