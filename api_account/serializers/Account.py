from rest_framework import serializers

from api_account.models import Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'


class AccountInfoSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source='role.name')

    class Meta:
        model = Account
        fields = ('id', 'first_name', 'last_name',
                 'username', 'email', 'is_staff',
                 'is_superuser', 'phone', 'age',
                 'address', 'avatar', 'role', 'is_active')