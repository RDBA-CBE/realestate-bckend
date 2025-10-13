from rest_framework import serializers
from ..models.adminprofile import AdminProfile

class AdminProfileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminProfile
        fields = ['id', 'user']

class AdminProfileDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminProfile
        fields = '__all__'

class AdminProfileCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminProfile
        fields = '__all__' 

class AdminProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminProfile
        fields = '__all__'
        read_only_fields = ['id', 'user']
