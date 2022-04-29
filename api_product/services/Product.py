import uuid
from datetime import datetime, timedelta


from django.db.models import Q

from api_product.constants import CategoryData
from api_product.models import Product
from api_product.serializers import ProductSerializer


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
