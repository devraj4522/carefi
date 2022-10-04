from rest_framework import serializers
from .models import User


class UserAccountSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserAccountSerializers_1(serializers.ModelSerializer):
    class Meta:
        model = User
        depth = 1
        fields = ('id', 'email', 'firstname', 'lastname', 'username')
