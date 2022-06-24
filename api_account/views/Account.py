import os

from django.contrib.auth.hashers import check_password, make_password
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from api_account.constants import RoleData
from api_account.models import Account
from api_account.permission import AdminOrManagerPermission, UserPermission, AdminPermission
from api_account.serializers import AccountInfoSerializer, GeneralInfoAccountSerializer, CreateAccountSerializer, \
    AdminGetAccountSerializer
from api_account.services import AccountService
from api_base.views import BaseViewSet


class AccountViewSet(BaseViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountInfoSerializer
    permission_classes = [UserPermission]

    serializer_map = {
        "get_account": AdminGetAccountSerializer,
    }

    permission_map = {
        "login": [],
        "list": [AdminOrManagerPermission],
        "create_employee": [AdminOrManagerPermission],
        "get_account": [AdminPermission],
        "edit_info": [AdminPermission],
        "delete": [AdminPermission],
        "reset_password": [AdminPermission]
    }

    @action(detail=False, methods=['post'])
    def login(self, request, *args, **kwargs):
        user_data = request.data
        username = user_data.get('username')
        password = user_data.get('password')

        account = Account.objects.filter(username=username)
        if account.exists():
            account = account.first()
            if not account.is_active:
                return Response({"details": "Account is disable.."}, status=status.HTTP_400_BAD_REQUEST)
            if check_password(password, account.password):
                token = RefreshToken.for_user(account)

                return Response({
                    "id": account.id,
                    "role": account.role.name,
                    "access_token": str(token.access_token),
                    "refresh_token": str(token)
                })
        return Response({"error_message": "invalid username/password"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def info(self, request, *args, **kwargs):
        user = request.user
        serializer = AccountInfoSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['patch'])
    def edit(self, request):
        user = request.user
        avatar = request.FILES.get('avatar')
        if avatar:
            avatar_link = AccountService.upload_avatar(avatar)
            request.data['avatar'] = avatar_link
        serializer = GeneralInfoAccountSerializer(user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            self.perform_update(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['patch'])
    def change_password(self, request, *args, **kwargs):
        account = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        if check_password(old_password, account.password):
            account.password = make_password(new_password)
            account.save()
            return Response({"detail": "Changed password!"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"error_message": "Old password is incorrect!"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def create_employee(self, request):
        request.data['role'] = RoleData.EMPLOYEE.value.get('id')
        request.data['password'] = os.getenv('DEFAULT_EMPLOYEE_PASSWORD')
        serialize = CreateAccountSerializer(data=request.data)
        if serialize.is_valid(raise_exception=True):
            serialize.save()
            return Response(serialize.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'])
    def get_account(self, request, pk):
        account = self.get_object()
        if account:
            return Response(AdminGetAccountSerializer(account).data, status=status.HTTP_200_OK)
        return Response({"error_message": "Account id is not defined!"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['patch'])
    def edit_info(self, request, pk):
        account = self.get_object()
        if account:
            avatar = request.FILES.get('avatar')
            if avatar:
                avatar_link = AccountService.upload_avatar(avatar)
                request.data['avatar'] = avatar_link
            serializer = AdminGetAccountSerializer(account, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"error_message": "Account id is not defined!"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'])
    def delete(self, request, pk):
        account = self.get_object()
        if account:
            account.delete()
            return Response({"details": "Completed delete account!"}, status=status.HTTP_200_OK)
        return Response({"error_message": "Account id is not defined!"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['put'])
    def edit_avatar(self, request):
        account = request.user
        if account:
            avatar = request.FILES.get('avatar')
            if avatar:
                avatar_link = AccountService.upload_avatar(avatar)
                request.data['avatar'] = avatar_link
                serializer = GeneralInfoAccountSerializer(account, data=request.data, partial=True)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({"error_message": "Avatar is not defined!"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error_message": "Account id is not defined!"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def reset_password(self, request, pk):
        account = self.get_object()
        if account:
            account.password = make_password(os.getenv('DEFAULT_EMPLOYEE_PASSWORD'))
            account.save()
            return Response({"success": "Reset password!"}, status=status.HTTP_200_OK)
        return Response({"error_message": "Account id is not defined!"}, status=status.HTTP_400_BAD_REQUEST)