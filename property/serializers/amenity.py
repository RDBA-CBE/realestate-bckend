from rest_framework import serializers
from common.serializers import BaseSerializer
from ..models import Amenity


class AmenityListSerializer(BaseSerializer):
    properties_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Amenity
        fields = ['id', 'name', 'description', 'properties_count', 'created_at']
    
    def get_properties_count(self, obj):
        return obj.properties.count()


class AmenityDetailSerializer(BaseSerializer):
    properties_count = serializers.SerializerMethodField()
    popular_property_types = serializers.SerializerMethodField()
    avg_property_price = serializers.SerializerMethodField()
    
    class Meta:
        model = Amenity
        fields = '__all__'
        extra_fields = ['properties_count', 'popular_property_types', 'avg_property_price']
    
    def get_properties_count(self, obj):
        return obj.properties.count()
    
    def get_popular_property_types(self, obj):
        from django.db.models import Count
        property_types = obj.properties.values(
            'property_type__name'
        ).annotate(
            count=Count('property_type')
        ).order_by('-count')[:5]
        
        return [
            {
                'type': item['property_type__name'], 
                'count': item['count']
            } 
            for item in property_types if item['property_type__name']
        ]
    
    def get_avg_property_price(self, obj):
        from django.db.models import Avg
        avg_price = obj.properties.aggregate(avg_price=Avg('price'))['avg_price']
        return round(avg_price, 2) if avg_price else 0


class AmenityCreateSerializer(BaseSerializer):
    class Meta:
        model = Amenity
        fields = ['name', 'description', 'category', 'icon', 'is_active']

class AmenityUpdateSerializer(BaseSerializer):
    class Meta:
        model = Amenity
        fields = ['name', 'description', 'category', 'icon', 'is_active']