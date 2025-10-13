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
        fields = ['name', 'description']
    
    def validate_name(self, value):
        if Amenity.objects.filter(name__iexact=value).exists():
            raise serializers.ValidationError("An amenity with this name already exists")
        return value


class AmenityUpdateSerializer(BaseSerializer):
    class Meta:
        model = Amenity
        fields = ['name', 'description']
    
    def validate_name(self, value):
        # Check if another amenity with this name exists (excluding current instance)
        if Amenity.objects.filter(name__iexact=value).exclude(pk=self.instance.pk).exists():
            raise serializers.ValidationError("An amenity with this name already exists")
        return value


class AmenityStatsSerializer(BaseSerializer):
    """Serializer for amenity usage statistics"""
    total_properties = serializers.SerializerMethodField()
    usage_percentage = serializers.SerializerMethodField()
    avg_property_price = serializers.SerializerMethodField()
    popular_cities = serializers.SerializerMethodField()
    
    class Meta:
        model = Amenity
        fields = ['id', 'name', 'total_properties', 'usage_percentage', 
                 'avg_property_price', 'popular_cities']
    
    def get_total_properties(self, obj):
        return obj.properties.count()
    
    def get_usage_percentage(self, obj):
        from ..models import Property
        total_properties = Property.objects.count()
        if total_properties == 0:
            return 0
        return round((obj.properties.count() / total_properties) * 100, 2)
    
    def get_avg_property_price(self, obj):
        from django.db.models import Avg
        avg_price = obj.properties.aggregate(avg_price=Avg('price'))['avg_price']
        return round(avg_price, 2) if avg_price else 0
    
    def get_popular_cities(self, obj):
        from django.db.models import Count
        cities = obj.properties.values('city').annotate(
            count=Count('city')
        ).order_by('-count')[:3]
        return [{'city': city['city'], 'count': city['count']} for city in cities]