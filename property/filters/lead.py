import django_filters
from ..models import Lead


class LeadFilter(django_filters.FilterSet):
    # Date filters
    created_after = django_filters.DateFilter(field_name='created_at', lookup_expr='gte')
    created_before = django_filters.DateFilter(field_name='created_at', lookup_expr='lte')
    next_follow_up_after = django_filters.DateTimeFilter(field_name='next_follow_up', lookup_expr='gte')
    next_follow_up_before = django_filters.DateTimeFilter(field_name='next_follow_up', lookup_expr='lte')

    # Budget filters
    budget_min_gte = django_filters.NumberFilter(field_name='budget_min', lookup_expr='gte')
    budget_min_lte = django_filters.NumberFilter(field_name='budget_min', lookup_expr='lte')
    budget_max_gte = django_filters.NumberFilter(field_name='budget_max', lookup_expr='gte')
    budget_max_lte = django_filters.NumberFilter(field_name='budget_max', lookup_expr='lte')

    # Text search filters
    search = django_filters.CharFilter(method='search_filter', label='Search')

    # Boolean filters
    has_follow_up = django_filters.BooleanFilter(field_name='next_follow_up', lookup_expr='isnull', exclude=True)
    is_active = django_filters.BooleanFilter(method='active_filter')

    class Meta:
        model = Lead
        fields = [
            'interested_property', 'status', 'priority', 'lead_source', 'assigned_to',
            'newsletter_subscribed', 'sms_marketing'
        ]

    def search_filter(self, queryset, name, value):
        """Search across multiple fields"""
        return queryset.filter(
            django_filters.Q(first_name__icontains=value) |
            django_filters.Q(last_name__icontains=value) |
            django_filters.Q(email__icontains=value) |
            django_filters.Q(phone__icontains=value) |
            django_filters.Q(company_name__icontains=value) |
            django_filters.Q(requirements__icontains=value)
        )

    def active_filter(self, queryset, name, value):
        """Filter for active leads (not won, lost, or cancelled)"""
        if value:
            return queryset.exclude(status__in=['won', 'lost', 'cancelled'])
        return queryset.filter(status__in=['won', 'lost', 'cancelled'])