from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api_base.views import BaseViewSet
from api_product.models import Category, Product
from api_product.serializers import CategorySerializer, ProductSerializer


class CategoryViewSet(BaseViewSet):
    queryset = Category.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = CategorySerializer

    @action(detail=True, methods=['get'])
    def get_products(self, request, pk):
        category = self.get_object()

        products = Product.objects.filter(category=category)
        if products.exists():
            rs = ProductSerializer(products, many=True)
            return Response(rs.data, status=status.HTTP_200_OK)
        else:
            return Response({"error_message": "product is not defined! "}, status=status.HTTP_400_BAD_REQUEST)

