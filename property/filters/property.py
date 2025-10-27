import django_filters
from django.db import models
from django.db.models import Q
from ..models import Property


class PropertyFilter(django_filters.FilterSet):
    min_area = django_filters.NumberFilter(field_name='total_area', lookup_expr='gte')
    max_area = django_filters.NumberFilter(field_name='total_area', lookup_expr='lte')
    min_rent = django_filters.NumberFilter(field_name='monthly_rent', lookup_expr='gte')
    max_rent = django_filters.NumberFilter(field_name='monthly_rent', lookup_expr='lte')
    
    sort_by = django_filters.OrderingFilter(
        fields=(
            ('title', 'title'),
            ("project__name", "project"),
            ('agent__first_name', 'agent'),
            ('developer__first_name', 'developer'),
            ("property_type__name", "property_type"),
            ("created_at", "created_at"),
            ("minimum_price", "minimum_price"),
            ("maximum_price", "maximum_price"),


        )
    )

    group = django_filters.CharFilter(method='filter_groups', help_text="Filter properties by group names")

    assigned_to_developer = django_filters.CharFilter(
        method='filter_assigned_to_developer',
        help_text="Filter properties assigned to a specific developer by developer's email"
    )
    assigned_to_agent = django_filters.CharFilter(
        method='filter_assigned_to_agent',
        help_text="Filter properties assigned to a specific agent by agent's email"
    )
    search = django_filters.CharFilter(
        method='filter_search',
        help_text="Search in title, description, address, city, state, and zip code"
    )
    min_price = django_filters.NumberFilter(field_name='minimum_price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='maximum_price', lookup_expr='lte')



    class Meta:
        model = Property
        fields = [
            'city', 'state', 'status', 'property_type', 'project', 'listing_type',
            'agent', 'bedrooms', 'bathrooms', 'furnishing', 'parking', 'facing_direction',
            'developer', 'land_type_zone', 'is_featured', 'is_verified', 'is_approved',
            'created_by', 'sort_by', 'search', 'group', 'min_price', 'max_price',
        ]

    def filter_search(self, queryset, name, value):
        """Search in title, description, address, city, state, and postal code"""
        return queryset.filter(
            Q(title__icontains=value) |
            Q(description__icontains=value) |
            Q(address__icontains=value) |
            Q(city__icontains=value) |
            Q(state__icontains=value) |
            Q(rera_id__icontains=value) |
            Q(postal_code__icontains=value)
        )
    
    def filter_assigned_to_developer(self, queryset, name, value):
        return queryset.filter(
            Q(developer_id=value) | Q(created_by_id=value)
        )

    def filter_assigned_to_agent(self, queryset, name, value):
        return queryset.filter(
            Q(agent_id=value) | Q(created_by_id=value)
        )

    def filter_groups(self, queryset, name, value):
        """Filter properties by group names"""
        group_names = [group.strip() for group in value.split(',')]
        return queryset.filter(
            Q(agent__groups__name__in=group_names) |
            Q(developer__groups__name__in=group_names) |
            Q(created_by__groups__name__in=group_names)
        ).distinct()



