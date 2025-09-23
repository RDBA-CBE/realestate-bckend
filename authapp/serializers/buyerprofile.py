from rest_framework import serializers
from ..models.buyerprofile import BuyerProfile

class BuyerProfileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuyerProfile
        fields = ['id', 'user', 'preferences']

class BuyerProfileDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuyerProfile
        fields = '__all__'

class BuyerProfileCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuyerProfile
        fields = ['user', 'preferences']

class BuyerProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuyerProfile
        fields = ['preferences']
