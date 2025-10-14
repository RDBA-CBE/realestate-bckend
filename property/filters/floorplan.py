import django_filters
from ..models import FloorPlan


class FloorPlanFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(lookup_expr='icontains')
    min_square_feet = django_filters.NumberFilter(field_name='square_feet', lookup_expr='gte')
    max_square_feet = django_filters.NumberFilter(field_name='square_feet', lookup_expr='lte')
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    rera_id = django_filters.CharFilter(lookup_expr='icontains')
    has_image = django_filters.BooleanFilter(field_name='image', lookup_expr='isnull', exclude=True)

    class Meta:
        model = FloorPlan
        fields = [
            'property', 'category', 'rera_id'
        ]