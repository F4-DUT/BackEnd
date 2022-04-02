from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from api_base.views import BaseViewSet
from api_product.models import ProductImage
from api_product.serializers import ProductImageSerializer


class ProductImageViewSet(BaseViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    permission_classes = [IsAuthenticated]

    permission_map = {
    }
