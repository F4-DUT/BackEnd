import uuid

from api_product.constants import CategoryData
from api_product.models import Product


class ProductService:

    @classmethod
    def create(cls, category):
        index = Product.objects.filter(category=category).count() + 1
        print(category.name)
        name = category.name + ' ' + str(index)
        status = True
        if category.name == CategoryData.DEFECTIVE_PRODUCT.value.get('name'):
            status = False
        product = Product(id=uuid.uuid4(), name=name, status=status, category=category)
        product.save()
        return product
