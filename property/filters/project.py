import django_filters
from django.db.models import Q
from ..models import Project

class ProjectFilter(django_filters.FilterSet):
    # Filter by the name of the groups the user belongs to
    group = django_filters.CharFilter(field_name='created_by__groups__name', lookup_expr='icontains')
    search = django_filters.CharFilter(method='filter_search', label='Search')

    class Meta:
        model = Project
        fields = [
            'name',
            'location',
            'developers',
            'status',
            'created_by',
            'group',  # now correctly mapped
            'search',  # custom search filter
        ]

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value) |
            Q(location__icontains=value)
        )