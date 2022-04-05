from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from api_base.views import BaseViewSet
from api_product.models import ProductImage
from api_product.serializers import ProductImageSerializer, ProductSerializer


class ProductImageViewSet(BaseViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    permission_classes = [IsAuthenticated]

    permission_map = {
    }

    @action(detail=True, methods=['get'])
    def get_product_by_image(self, request, pk):
        product = self.get_object().product
        serializer = ProductSerializer(product)
        if serializer:
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"error_message": "Product is not defined!!"}, status=status.HTTP_400_BAD_REQUEST)
