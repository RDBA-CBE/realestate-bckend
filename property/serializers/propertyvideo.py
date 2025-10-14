from rest_framework import serializers
from ..models import PropertyVideo

class PropertyVideoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyVideo
        fields = ['id', 'title', 'thumbnail','video','duration', 'order', 'created_at']

class PropertyVideoDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyVideo
        fields = '__all__'

class PropertyVideoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyVideo
        fields = ['id', 'property', 'video', 'title', 'description', 'thumbnail', 'duration', 'order']

class PropertyVideoUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyVideo
        fields = ['title', 'description', 'thumbnail', 'duration', 'order']