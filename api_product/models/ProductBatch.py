from django.db import models

from api_account.models import Account
from api_base.models import TimeStampedModel


class ProductBatch(TimeStampedModel):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="product_batches")
