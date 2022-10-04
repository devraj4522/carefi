from rest_framework import serializers
from .models import Bitcoin


class BitcoinAccountSerializers(serializers.ModelSerializer):
    class Meta:
        model = Bitcoin
        fields = '__all__'


class BitcoinAccountSerializers_1(serializers.ModelSerializer):
    class Meta:
        model = Bitcoin
        depth = 1
        fields = ('id', 'price', 'time')
