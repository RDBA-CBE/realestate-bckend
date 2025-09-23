from rest_framework import serializers
from ..models.propertyimage import PropertyImage

class PropertyImageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = ['id', 'property', 'image', 'is_primary', 'order']

class PropertyImageDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = '__all__'

class PropertyImageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = ['property', 'image', 'alt_text', 'caption', 'is_primary', 'order']

class PropertyImageUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = ['alt_text', 'caption', 'is_primary', 'order']
