from rest_framework import serializers
from ..models import VirtualTour

class VirtualTourListSerializer(serializers.ModelSerializer):
    class Meta:
        model = VirtualTour
        fields = ['id', 'tour_type', 'provider', 'thumbnail', 'is_active', 'order', 'created_at']

class VirtualTourDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = VirtualTour
        fields = '__all__'

class VirtualTourCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = VirtualTour
        fields = [
            'property', 'tour_url', 'tour_type', 'description', 
            'thumbnail', 'provider', 'embed_code', 'is_active', 'order'
        ]

class VirtualTourUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = VirtualTour
        fields = [
            'tour_url', 'tour_type', 'description', 
            'thumbnail', 'provider', 'embed_code', 'is_active', 'order'
        ]