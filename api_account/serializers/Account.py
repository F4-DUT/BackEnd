from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from api_account.models import Account


class AccountInfoSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source='role.name')

    class Meta:
        model = Account
        fields = ('id', 'first_name', 'last_name',
                 'username', 'email', 'is_staff',
                 'is_superuser', 'phone', 'age',
                 'address', 'avatar', 'role', 'is_active')


class GeneralInfoAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        exclude = ('password', 'role', 'is_active', 'is_staff', 'is_superuser')


class CreateAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'username', 'password', 'email', 'role')

    def validate(self, attrs):
        password = attrs.get('password')
        attrs['password'] = make_password(password)
        return attrs
