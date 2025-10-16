import django_filters
from django.db import models
from ..models import Property

class PropertyFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    min_area = django_filters.NumberFilter(field_name='total_area', lookup_expr='gte')
    max_area = django_filters.NumberFilter(field_name='total_area', lookup_expr='lte')
    min_rent = django_filters.NumberFilter(field_name='monthly_rent', lookup_expr='gte')
    max_rent = django_filters.NumberFilter(field_name='monthly_rent', lookup_expr='lte')
    sort_by = django_filters.OrderingFilter(
        fields=(
            ('price', 'price'),
            ('title', 'title'),
            ("project__name", "project"),
            ('agent__first_name', 'agent'),
            ('developer__first_name', 'developer'),
            ("property_type__name", "property type"),
            ("created_at", "created_at")
        )
    )
    search = django_filters.CharFilter(
        method='filter_search',
        help_text="Search in title, description, address, city, state, and zip code"
    )
    
    class Meta:
        model = Property
        fields = [
            'city', 'state', 'status', 'property_type', 'project', 'listing_type','agent', 
            'bedrooms', 'bathrooms', 'furnishing', 'parking', 'facing_direction','developer',
            'land_type_zone', 'is_featured', 'is_verified', 'is_approved', 'created_by', 'sort_by',
            'search'
        ]

    def filter_search(self, queryset, name, value):
        """Search in title, description, address, city, state, and zip code"""
        
        return queryset.filter(
            models.Q(title__icontains=value) |
            models.Q(description__icontains=value) |
            models.Q(address__icontains=value) |
            models.Q(city__icontains=value) |
            models.Q(state__icontains=value) |
            models.Q(rera_id__icontains=value) |
            models.Q(postal_code__icontains=value)
        )