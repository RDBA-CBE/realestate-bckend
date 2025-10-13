from rest_framework import serializers
from ..models import PropertyType


class PropertyTypeListSerializer(serializers.ModelSerializer):
    properties_count = serializers.SerializerMethodField()
    avg_price = serializers.SerializerMethodField()
    
    class Meta:
        model = PropertyType
        fields = ['id', 'name', 'description', 'properties_count', 'avg_price']
    
    def get_properties_count(self, obj):
        return obj.properties.count()
    
    def get_avg_price(self, obj):
        from django.db.models import Avg
        avg_price = obj.properties.aggregate(avg_price=Avg('price'))['avg_price']
        return round(avg_price, 2) if avg_price else 0


class PropertyTypeDetailSerializer(serializers.ModelSerializer):
    properties_count = serializers.SerializerMethodField()
    available_properties = serializers.SerializerMethodField()
    sold_properties = serializers.SerializerMethodField()
    avg_price = serializers.SerializerMethodField()
    min_price = serializers.SerializerMethodField()
    max_price = serializers.SerializerMethodField()
    popular_cities = serializers.SerializerMethodField()
    
    class Meta:
        model = PropertyType
        fields = '__all__'
        extra_fields = [
            'properties_count', 'available_properties', 'sold_properties',
            'avg_price', 'min_price', 'max_price', 'popular_cities'
        ]
    
    def get_properties_count(self, obj):
        return obj.properties.count()
    
    def get_available_properties(self, obj):
        return obj.properties.filter(status='available').count()
    
    def get_sold_properties(self, obj):
        return obj.properties.filter(status='sold').count()
    
    def get_avg_price(self, obj):
        from django.db.models import Avg
        avg_price = obj.properties.aggregate(avg_price=Avg('price'))['avg_price']
        return round(avg_price, 2) if avg_price else 0
    
    def get_min_price(self, obj):
        from django.db.models import Min
        min_price = obj.properties.aggregate(min_price=Min('price'))['min_price']
        return min_price if min_price else 0
    
    def get_max_price(self, obj):
        from django.db.models import Max
        max_price = obj.properties.aggregate(max_price=Max('price'))['max_price']
        return max_price if max_price else 0
    
    def get_popular_cities(self, obj):
        from django.db.models import Count
        cities = obj.properties.values('city').annotate(
            count=Count('city')
        ).order_by('-count')[:5]
        return [{'city': city['city'], 'count': city['count']} for city in cities]


class PropertyTypeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyType
        fields = ['name', 'description']
    
    def validate_name(self, value):
        if PropertyType.objects.filter(name__iexact=value).exists():
            raise serializers.ValidationError("A property type with this name already exists")
        return value


class PropertyTypeUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyType
        fields = ['name', 'description']
    
    def validate_name(self, value):
        # Check if another property type with this name exists (excluding current instance)
        if PropertyType.objects.filter(name__iexact=value).exclude(pk=self.instance.pk).exists():
            raise serializers.ValidationError("A property type with this name already exists")
        return value


class PropertyTypeStatsSerializer(serializers.ModelSerializer):
    """Serializer for property type statistics"""
    total_properties = serializers.SerializerMethodField()
    total_value = serializers.SerializerMethodField()
    avg_area = serializers.SerializerMethodField()
    price_range = serializers.SerializerMethodField()
    status_breakdown = serializers.SerializerMethodField()
    
    class Meta:
        model = PropertyType
        fields = ['id', 'name', 'total_properties', 'total_value', 'avg_area', 
                 'price_range', 'status_breakdown']
    
    def get_total_properties(self, obj):
        return obj.properties.count()
    
    def get_total_value(self, obj):
        from django.db.models import Sum
        total = obj.properties.aggregate(total=Sum('price'))['total']
        return total if total else 0
    
    def get_avg_area(self, obj):
        from django.db.models import Avg
        avg_area = obj.properties.aggregate(avg_area=Avg('total_area'))['avg_area']
        return round(avg_area, 2) if avg_area else 0
    
    def get_price_range(self, obj):
        from django.db.models import Min, Max
        price_range = obj.properties.aggregate(
            min_price=Min('price'),
            max_price=Max('price')
        )
        return {
            'min': price_range['min_price'] if price_range['min_price'] else 0,
            'max': price_range['max_price'] if price_range['max_price'] else 0
        }
    
    def get_status_breakdown(self, obj):
        from django.db.models import Count
        status_counts = obj.properties.values('status').annotate(
            count=Count('status')
        )
        return {item['status']: item['count'] for item in status_counts}