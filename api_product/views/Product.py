from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api_base.views import BaseViewSet
from api_product.models import Product, Category
from api_product.serializers import ProductSerializer


class ProductViewSet(BaseViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    permission_map = {

    }

    @action(detail=False, methods=['get'])
    def get_list_by_category(self, request):
        category = Category.objects.filter(id=request.data.get('category_id')).first()

        products = Product.objects.filter(category=category)
        if products.exists():
            rs = ProductSerializer(products, many=True)
            return Response(rs.data, status=status.HTTP_200_OK)
        else:
            return Response({"error_message": "product is not defined! "}, status=status.HTTP_400_BAD_REQUEST)
