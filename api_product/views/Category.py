from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from api_account.permission import UserPermission, EmployeePermission
from api_base.pagination import CustomPagePagination
from api_base.views import BaseViewSet
from api_product.constants import CategoryData
from api_product.models import Category, Product, Dataset
from api_product.serializers import CategorySerializer, ProductSerializer, DatasetSerializer


class CategoryViewSet(BaseViewSet):
    queryset = Category.objects.all()
    permission_classes = [UserPermission, EmployeePermission]
    serializer_class = CategorySerializer
    pagination_class = CustomPagePagination

    @action(detail=True, methods=['get'])
    def get_products(self, request, pk):
        category = self.get_object()

        if category:
            products = Product.objects.filter(category=category)
            if products.exists():
                rs = ProductSerializer(products, many=True)
                return Response(rs.data, status=status.HTTP_200_OK)
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