from rest_framework import serializers
from ..models.property import Amenity

class AmenityListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = ['id', 'has_balcony', 'has_garden', 'has_swimming_pool', 'has_gym', 'has_elevator', 'has_security', 'has_power_backup', 'has_air_conditioning', 'pet_friendly']

class AmenityDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = '__all__'

class AmenityCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = ['has_balcony', 'has_garden', 'has_swimming_pool', 'has_gym', 'has_elevator', 'has_security', 'has_power_backup', 'has_air_conditioning', 'pet_friendly']

class AmenityUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = ['has_balcony', 'has_garden', 'has_swimming_pool', 'has_gym', 'has_elevator', 'has_security', 'has_power_backup', 'has_air_conditioning', 'pet_friendly']
