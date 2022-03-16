from django.contrib.auth.hashers import check_password
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from api_account.models import Account
from api_account.serializers import AccountSerializer, AccountInfoSerializer, GeneralInfoAccountSerializer
from api_account.services import AccountService
from api_base.views import BaseViewSet


class AccountViewSet(BaseViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountInfoSerializer
    permission_classes = [IsAuthenticated]

    permission_map = {
        "login": [],
        "signup": []
    }

    @action(detail=False, methods=['post'])
    def login(self, request):
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
                }, status=status.HTTP_200_OK)
        return Response({"error_message": "invalid username/password"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def info(self, request):
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

