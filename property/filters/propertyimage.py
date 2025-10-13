import django_filters
from ..models import PropertyImage


class PropertyImageFilter(django_filters.FilterSet):
    alt_text = django_filters.CharFilter(lookup_expr='icontains')
    caption = django_filters.CharFilter(lookup_expr='icontains')
    min_order = django_filters.NumberFilter(field_name='order', lookup_expr='gte')
    max_order = django_filters.NumberFilter(field_name='order', lookup_expr='lte')
    has_alt_text = django_filters.BooleanFilter(field_name='alt_text', lookup_expr='isnull', exclude=True)
    has_caption = django_filters.BooleanFilter(field_name='caption', lookup_expr='isnull', exclude=True)
    
    class Meta:
        model = PropertyImage
        fields = [
            'property', 'is_primary', 'order'
        ]