import django_filters
from django.db import models
from django.db.models import Q
from ..models import PropertyWishlist   


class PropertyWishlistFilter(django_filters.FilterSet):
    """Filter for property wishlists"""
    is_public = django_filters.BooleanFilter()
    created_after = django_filters.DateFilter(field_name='created_at', lookup_expr='gte')
    created_before = django_filters.DateFilter(field_name='created_at', lookup_expr='lte')
    properties = django_filters.CharFilter(method='properties_filter', label='Properties')

    class Meta:
        model = PropertyWishlist
        fields = ['is_public', 'created_after', 'created_before', 'properties']
    
    def properties_filter(self, queryset, name, value):
        """Filter wishlists containing specific property IDs (comma-separated)"""
        property_ids = [int(pid) for pid in value.split(',') if pid.isdigit()]
        return queryset.filter(properties__id__in=property_ids).distinct()