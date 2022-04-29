from datetime import datetime

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from api_account.permission import RaspberryPermission, UserPermission
from api_base.views import BaseViewSet
from api_product.constants import CategoryData
from api_product.models import Product, Category, ProductImage
from api_product.serializers import ProductSerializer, CategorySerializer, ProductImageSerializer
from api_product.services import ProductImageService, CategoryService, ProductService


class ProductViewSet(BaseViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [UserPermission]

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

    @action(detail=False, methods=['post'])
    def get_product_by_status(self, request):
        status_product = request.data.get('status')
        if status_product:
            products = Product.objects.filter(status=status_product)
            serializers = ProductSerializer(products, many=True)
            return Response(serializers.data, status=status.HTTP_200_OK)
        return Response({"error_message": "status is required!"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def get_image(self, request, pk):
        product = self.get_object()
        if product:
            images = ProductImage.objects.filter(product=product)
            serializers = ProductImageSerializer(images, many=True)
            return Response(serializers.data, status=status.HTTP_200_OK)
        return Response({"error_message": "product is not defined!"}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=False)
    def get_product_statistics(self, request, *args, **kwargs):
        start_date = request.query_params.get("start_date", "")
        end_date = request.query_params.get("end_date", "")

        if not start_date or not end_date:
            return Response({"detail": "Not found start_date and end_date in url param"},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
            if start_date > end_date:
                raise ValueError
        except ValueError:
            return Response({"detail": "Invalid start_date/end_date"}, status=status.HTTP_400_BAD_REQUEST)

        product_statistics = ProductService.get_product_statistics(start_date, end_date)
        return Response(product_statistics)
