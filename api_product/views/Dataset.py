from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from api_account.permission import ManagerPermission, UserPermission
from api_base.pagination import CustomPagePagination
from api_base.views import BaseViewSet
from api_product.models import Dataset, Category
from api_product.serializers import DatasetSerializer
from api_product.services import DatasetService


class DatasetViewSet(BaseViewSet):
    queryset = Dataset.objects.all()
    permission_classes = [UserPermission]
    pagination_class = [CustomPagePagination]

    permission_map = {
        'change_model': [ManagerPermission]
    }




