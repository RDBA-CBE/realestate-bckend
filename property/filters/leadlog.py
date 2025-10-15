import django_filters
from ..models import LeadLog


class LeadLogFilter(django_filters.FilterSet):
    """Simple filter for lead logs"""
    
    # Basic filters
    lead = django_filters.NumberFilter(field_name='lead__id')
    action = django_filters.ChoiceFilter(choices=LeadLog.ACTION_CHOICES)
    performed_by = django_filters.NumberFilter(field_name='performed_by__id')
    
    # Date filters
    date_from = django_filters.DateTimeFilter(
        field_name='created_at',
        lookup_expr='gte'
    )
    date_to = django_filters.DateTimeFilter(
        field_name='created_at',
        lookup_expr='lte'
    )
    
    # Text search
    search = django_filters.CharFilter(
        method='filter_search',
        help_text="Search in description and notes"
    )

    class Meta:
        model = LeadLog
        fields = ['lead', 'action', 'performed_by']

    def filter_search(self, queryset, name, value):
        """Search in description and notes"""
        from django.db import models
        return queryset.filter(
            models.Q(description__icontains=value) |
            models.Q(notes__icontains=value)
        )