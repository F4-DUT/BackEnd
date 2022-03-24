from rest_framework.permissions import IsAuthenticated

from api_base.views import BaseViewSet
from api_product.models import Product
from api_product.serializers.Product import ProductSerializer


class ProductViewSet(BaseViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    permission_map = {

    }