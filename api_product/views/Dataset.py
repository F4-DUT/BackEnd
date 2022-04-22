from rest_framework.decorators import action

from api_account.permission import ManagerPermission, UserPermission
from api_base.views import BaseViewSet
from api_product.models import Dataset


class DatasetViewSet(BaseViewSet):
    queryset = Dataset.objects.all()
    permission_classes = [UserPermission]

    permission_map = {
        'change_model': [ManagerPermission]
    }


