from rest_framework import serializers


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = 'Account'
        field = '__all__'
