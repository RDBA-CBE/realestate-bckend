import django_filters
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
    
    class Meta:
        model = Property
        fields = [
            'city', 'state', 'status', 'property_type', 'project', 'listing_type',
            'bedrooms', 'bathrooms', 'furnishing', 'parking', 'facing_direction',
            'land_type_zone', 'is_featured', 'is_verified', 'is_approved', 'created_by', 'sort_by'
        ]
