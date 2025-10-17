import django_filters
from django.db import models
from django.db.models import Q
from ..models import PropertyWishlist   


class PropertyWishlistFilter(django_filters.FilterSet):
    """Filter for property wishlists"""
    is_public = django_filters.BooleanFilter()
    created_after = django_filters.DateFilter(field_name='created_at', lookup_expr='gte')
    created_before = django_filters.DateFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = PropertyWishlist
        fields = ['is_public', 'created_after', 'created_before']