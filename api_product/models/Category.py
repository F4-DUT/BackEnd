from django.db import models

from api_base.models import TimeStampedModel


class Category(TimeStampedModel):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'category'

