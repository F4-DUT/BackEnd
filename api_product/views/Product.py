from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api_account.permission import RaspberryPermission
from api_base.views import BaseViewSet
from api_product.models import Product, Category
from api_product.serializers import ProductSerializer




class ProductViewSet(BaseViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    permission_map = {
        "send_image": [RaspberryPermission]
    }






