from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from api_account.permission import RaspberryPermission, UserPermission
from api_base.views import BaseViewSet
from api_product.models import Product, Category, ProductImage
from api_product.serializers import ProductSerializer, CategorySerializer, ProductImageSerializer
from api_product.services import ProductImageService, CategoryService, ProductService


class ProductViewSet(BaseViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [UserPermission]

    permission_map = {
        "send_image": [RaspberryPermission],
        "send_images": [RaspberryPermission]
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
    def send_images(self, request, *args, **kwargs):
        image1 = request.FILES.get('image1')
        image2 = request.FILES.get('image2')
        if image1 and image2:
            images = [image1, image2]
            image_urls = ProductImageService.upload_images(images)
            category = CategoryService.check_category(image1)   #not check 2 image
            product = ProductService.create(category)
            ProductImageService.create(image_urls, product)
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