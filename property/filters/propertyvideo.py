import django_filters
from ..models import PropertyVideo


class PropertyVideoFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    description = django_filters.CharFilter(lookup_expr='icontains')
    min_duration = django_filters.DurationFilter(field_name='duration', lookup_expr='gte')
    max_duration = django_filters.DurationFilter(field_name='duration', lookup_expr='lte')
    min_file_size = django_filters.NumberFilter(field_name='file_size', lookup_expr='gte')
    max_file_size = django_filters.NumberFilter(field_name='file_size', lookup_expr='lte')
    min_order = django_filters.NumberFilter(field_name='order', lookup_expr='gte')
    max_order = django_filters.NumberFilter(field_name='order', lookup_expr='lte')
    has_thumbnail = django_filters.BooleanFilter(field_name='thumbnail', lookup_expr='isnull', exclude=True)
    
    class Meta:
        model = PropertyVideo
        fields = [
            'property', 'order'
        ]