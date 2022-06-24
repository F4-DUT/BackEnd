from api_account.models import Role
from api_account.permission import AdminOrManagerPermission
from api_account.serializers import RoleSerializer
from api_base.views import BaseViewSet


class RoleViewSet(BaseViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [AdminOrManagerPermission]