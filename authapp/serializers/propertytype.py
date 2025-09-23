from rest_framework import serializers
from ..models.property import PropertyType

class PropertyTypeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyType
        fields = ['id', 'name']

class PropertyTypeDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyType
        fields = '__all__'

class PropertyTypeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyType
        fields = ['name', 'description']

class PropertyTypeUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyType
        fields = ['name', 'description']
