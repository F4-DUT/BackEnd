from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api_account.permission import RaspberryPermission
from api_base.views import BaseViewSet
from api_product.models import Product, Category
from api_product.serializers import ProductSerializer, CategorySerializer
from api_product.services import ProductImageService, CategoryService, ProductService


class ProductViewSet(BaseViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    permission_map = {
        "send_image": [RaspberryPermission]
    }

    @action(detail=False, methods=['post'])
    def send_image(self, request, *args, **kwargs):
        image = request.FILES.get('image')
        if image:
            image_url = ProductImageService.upload_image(image)
            category = CategoryService.check_category(image)
            product = ProductService.create(category)
            ProductImageService.create(image_url, product)
            return Response(ProductSerializer(product).data, status=status.HTTP_200_OK)
        return Response({"error_message": "image is not defined!!"})
