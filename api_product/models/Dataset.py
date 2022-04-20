from django.db import models

from api_base.models import TimeStampedModel
from api_product.models import Category


class Dataset(TimeStampedModel):
    url = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="datasets", null=True, blank=True)

    class Meta:
        db_table = 'dataset'
        ordering = ('created_at',)
