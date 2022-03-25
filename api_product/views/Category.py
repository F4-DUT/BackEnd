from rest_framework.permissions import IsAuthenticated

from api_base.views import BaseViewSet
from api_product.models import Category
from api_product.serializers import CategorySerializer


class CategoryViewSet(BaseViewSet):
    queryset = Category.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = CategorySerializer

