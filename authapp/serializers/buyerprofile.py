from rest_framework import serializers
from ..models.buyerprofile import BuyerProfile

class BuyerProfileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuyerProfile
        fields = '__all__'

class BuyerProfileDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuyerProfile
        fields = '__all__'

class BuyerProfileCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuyerProfile
        fields = "__all__"

class BuyerProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuyerProfile
        fields = "__all__"
