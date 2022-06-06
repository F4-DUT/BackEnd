from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from api_account.permission import UserPermission, EmployeePermission
from api_base.pagination import CustomPagePagination
from api_base.views import BaseViewSet
from api_product.constants import CategoryData
from api_product.models import Category, Product, Dataset
from api_product.serializers import CategorySerializer, ProductSerializer, DatasetSerializer
from api_product.services import DatasetService


class CategoryViewSet(BaseViewSet):
    queryset = Category.objects.all()
    permission_classes = [UserPermission]
    serializer_class = CategorySerializer
    pagination_class = CustomPagePagination

    @action(detail=True, methods=['get'])
    def get_products(self, request, pk):
        category = self.get_object()
        if category:
            products = Product.objects.filter(category=category)
            if products.exists():
                page = self.paginate_queryset(products)
                if page is not None:
                    rs = ProductSerializer(page, many=True)
                    return self.get_paginated_response(rs.data)
                res = ProductSerializer(page, many=True)
                return Response({'detail': res.data}, status=status.HTTP_200_OK)
            else:
                return Response({"error_message": "product is not defined! "}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error_message": "category is not defined!"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def get_dataset(self, request, pk):
        category = self.get_object()

        if category:
            datasets = Dataset.objects.filter(category=category)
            if datasets.exists():
                page = self.paginate_queryset(datasets)
                if page is not None:
                    res = DatasetSerializer(page, many=True)
                    return self.get_paginated_response(res.data)
                res = DatasetSerializer(page, many=True)
                return Response({'detail': res.data}, status=status.HTTP_200_OK)
            else:
                return Response({"error_message": "dataset is not defined!"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error_message": "category is not defined!"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def upload_dataset(self, request, pk):
        category = self.get_object()
        if category:
            images = request.FILES.getlist('images')
            print(images)
            request.data._mutable = True
            image_urls = DatasetService.upload_images(images, category)
            DatasetService.create(image_urls, category)
            rs = Dataset.objects.filter(category=category)
            page = self.paginate_queryset(rs)
            if page is not None:
                res = DatasetSerializer(page, many=True)
                return self.get_paginated_response(res.data)
            res = DatasetSerializer(page, many=True)
            return Response({'detail': res.data}, status=status.HTTP_200_OK)
        return Response({'error_message': "Category is not defined!"}, status=status.HTTP_400_BAD_REQUEST)
