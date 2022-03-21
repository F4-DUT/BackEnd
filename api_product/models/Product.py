from django.db import models

from api_base.models import TimeStampedModel
from api_product.models import ProductBatch


class Product(TimeStampedModel):
    name = models.CharField(max_length=50)
    status = models.BooleanField(null=True, blank=True)

    product_batch = models.ForeignKey(ProductBatch, on_delete=models.CASCADE, related_name="products")
