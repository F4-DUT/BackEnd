import uuid
from datetime import datetime, timedelta
import time

from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response

from api_product.constants import CategoryData
from api_product.models import Product
from api_product.serializers import ProductSerializer
from api_product.utils import DateTime


class ProductService:

    @classmethod
    def create(cls, category):
        index = Product.objects.filter(category=category).count() + 1
        print(category.name)
        name = category.name + ' ' + str(index)
        status = True
        if category.name == CategoryData.DEFECTIVE_PRODUCT1.value.get(
                'name') or category.name == CategoryData.DEFECTIVE_PRODUCT2.value.get('name'):
            status = False
        product = Product(id=uuid.uuid4(), name=name, status=status, category=category)
        product.save()
        return product

    @classmethod
    def get_product_statistics(cls, start_date, end_date):
        response = []
        date = start_date
        while date <= end_date:
            products = Product.objects.filter(updated_at__gte=datetime.combine(date, datetime.min.time()),
                                              updated_at__lte=datetime.combine(date, datetime.max.time()))
            valid_count = 0
            invalid_count = 0
            if products.exists():
                for product in products:
                    if product.status:
                        valid_count += 1
                    else:
                        invalid_count += 1
            response.append({
                "day": date,
                "valid": valid_count,
                "invalid": invalid_count
            })
            date = date + timedelta(days=1)
        return response
        return {"error_message": "no product"}

    @classmethod
    def get_accuracy(cls, products):
        invalid = 0
        valid = 0
        for product in products:
            if product.status:
                valid += 1
            else:
                invalid += 1
        return [valid, invalid, valid/products.count()*100]

    @classmethod
    def get_system_accuracy(cls):
        products = Product.objects.all()
        if products.exists():
            [valid, invalid, accuracy] = cls.get_accuracy(products)
            return {
                "valid": valid,
                "invalid": invalid,
                "system_accuracy": accuracy
            }
        return Response({"error_message": "fail to load products"}, status=status.HTTP_400_BAD_REQUEST)

    @classmethod
    def get_month_accuracy(cls):
        month = datetime.now().month
        nearly_month = month-1
        nearly_month_start_date = datetime(datetime.now().year, nearly_month, 1, 0, 0, 1)
        nearly_month_end_date = datetime(datetime.now().year, nearly_month, DateTime.last_day_of_month(datetime.now().year, nearly_month), 23, 59, 59)
        nearly_month_products = Product.objects.filter(updated_at__gte=nearly_month_start_date,
                                          updated_at__lte=nearly_month_end_date)
        
        start_date = datetime(datetime.now().year, month, 1, 0, 0, 1)
        end_date = datetime(datetime.now().year, month, datetime.now().day, 23, 59, 59)
        products = Product.objects.filter(updated_at__gte=start_date,
                                          updated_at__lte=end_date)
        if nearly_month_products:
            [valid, invalid, accuracy] = cls.get_accuracy(nearly_month_products)
        else:
            [valid, invalid, accuracy] = [0, 0, 0]
        if products:
            [_valid, _invalid, _accuracy] = cls.get_accuracy(products)
        else:
            [_valid, _invalid, _accuracy] = [0, 0, 0]

        accuracy_difference = _accuracy - accuracy
        return {
            "nearly_month_accuracy": accuracy,
            "month_accuracy": _accuracy,
            "accuracy_difference": accuracy_difference
        }

    @classmethod
    def get_week_accuracy(cls):
        wday_today = time.localtime(time.time()).tm_wday + 1
        nearly_week_start_date = datetime(datetime.now().year, datetime.now().month, datetime.now().day, 0, 0, 1) - timedelta(days=wday_today+7)
        nearly_week_end_date = datetime(datetime.now().year, datetime.now().month, datetime.now().day, 23, 59, 59) - timedelta(days=wday_today)

        nearly_week_products = Product.objects.filter(updated_at__gte=nearly_week_start_date,
                                          updated_at__lte=nearly_week_end_date)

        start_date = datetime(datetime.now().year, datetime.now().month, datetime.now().day, 0, 0, 1) - timedelta(days=wday_today)
        end_date = datetime(datetime.now().year, datetime.now().month, datetime.now().day, 23, 59, 59)

        products = Product.objects.filter(updated_at__gte=start_date,
                                          updated_at__lte=end_date)

        if nearly_week_products:
            [valid, invalid, accuracy] = cls.get_accuracy(nearly_week_products)
        else:
            [valid, invalid, accuracy] = [0, 0, 0]
        if products:
            [_valid, _invalid, _accuracy] = cls.get_accuracy(products)
        else:
            [_valid, _invalid, _accuracy] = [0, 0, 0]

        accuracy_difference = _accuracy-accuracy
        return {
            "nearly_week_accuracy": accuracy,
            "week_accuracy": _accuracy,
            "accuracy_difference": accuracy_difference
        }

    @classmethod
    def get_AI_accuracy(cls):
        return {
                "accuracy": 81.49,
                "old_accuracy": 80.01,
                "accuracy_difference": 1.48
        }