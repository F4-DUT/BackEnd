
from django.contrib.auth.models import AbstractUser, UserManager
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from api_account.models import Role


class Account(AbstractUser):
    objects = UserManager()
    username = models.CharField(max_length=20, unique=True)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    avatar = models.CharField(max_length=255, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=11, null=True, blank=True)
    age = models.IntegerField(validators=[MaxValueValidator(70), MinValueValidator(18)], null=True, blank=True)

    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='accounts')

    USERNAME_FIELD = 'username'

    class Meta:
        db_table = 'account'
