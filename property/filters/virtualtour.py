import django_filters
from ..models import VirtualTour


class VirtualTourFilter(django_filters.FilterSet):
    tour_url = django_filters.CharFilter(lookup_expr='icontains')
    description = django_filters.CharFilter(lookup_expr='icontains')
    provider = django_filters.CharFilter(lookup_expr='icontains')
    min_order = django_filters.NumberFilter(field_name='order', lookup_expr='gte')
    max_order = django_filters.NumberFilter(field_name='order', lookup_expr='lte')
    has_thumbnail = django_filters.BooleanFilter(field_name='thumbnail', lookup_expr='isnull', exclude=True)
    has_embed_code = django_filters.BooleanFilter(field_name='embed_code', lookup_expr='isnull', exclude=True)
    
    class Meta:
        model = VirtualTour
        fields = [
            'property', 'tour_type', 'is_active', 'order'
        ]