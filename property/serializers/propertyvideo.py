from rest_framework import serializers
from ..models import PropertyVideo

class PropertyVideoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyVideo
        fields = ['id', 'title', 'thumbnail', 'duration', 'order', 'created_at']

class PropertyVideoDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyVideo
        fields = '__all__'

class PropertyVideoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyVideo
        fields = ['property', 'video', 'title', 'description', 'thumbnail', 'duration', 'order']

class PropertyVideoUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyVideo
        fields = ['title', 'description', 'thumbnail', 'duration', 'order']