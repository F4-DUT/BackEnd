from api_account.permission import ManagerPermission
from api_base.views import BaseViewSet
from api_product.models import Dataset


class DatasetViewSet(BaseViewSet):
    queryset = Dataset.objects.all()
    permission_classes = [ManagerPermission]

