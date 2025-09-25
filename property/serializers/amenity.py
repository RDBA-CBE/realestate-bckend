from rest_framework import serializers
from common.serializers import BaseSerializer
from ..models import Amenity

class AmenityListSerializer(BaseSerializer):
    class Meta:
        model = Amenity
        fields = "__all__"

class AmenityDetailSerializer(BaseSerializer):
    class Meta:
        model = Amenity
        fields = '__all__'

class AmenityCreateSerializer(BaseSerializer):
    class Meta:
        model = Amenity
        fields = ['name', 'description', 'category', 'icon', 'is_active']

class AmenityUpdateSerializer(BaseSerializer):
    class Meta:
        model = Amenity
        fields = ['name', 'description', 'category', 'icon', 'is_active']