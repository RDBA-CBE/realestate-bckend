from rest_framework import serializers
from ..models.developerprofile import DeveloperProfile

class DeveloperProfileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeveloperProfile
        fields = ['id', 'user', 'company_name']

class DeveloperProfileDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeveloperProfile
        fields = '__all__'

class DeveloperProfileCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeveloperProfile
        fields = ['user', 'company_name']

class DeveloperProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeveloperProfile
        fields = ['company_name']
