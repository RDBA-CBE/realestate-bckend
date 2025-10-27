import django_filters
from django.db.models import Q
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

    property_type = django_filters.CharFilter(field_name='interested_property__property_type', lookup_expr='iexact')
    group = django_filters.BaseInFilter(method='group_filter', label='Group')

    assigned_to_group = django_filters.BaseInFilter(field_name='assigned_to__groups__id', lookup_expr='in')
    created_by_group = django_filters.BaseInFilter(field_name='created_by__groups__id', lookup_expr='in')
    # Text search filters
    search = django_filters.CharFilter(method='search_filter', label='Search')

    # Boolean filters
    has_follow_up = django_filters.BooleanFilter(field_name='next_follow_up', lookup_expr='isnull', exclude=True)
    is_active = django_filters.BooleanFilter(method='active_filter')


    class Meta:
        model = Lead
        fields = "__all__"

    def search_filter(self, queryset, name, value):
        """Search across multiple fields"""
        return queryset.filter(
            Q(first_name__icontains=value) |
            Q(last_name__icontains=value) |
            Q(email__icontains=value) |
            Q(phone__icontains=value) |
            Q(company_name__icontains=value) |
            Q(requirements__icontains=value) |
            Q(interested_property__title__icontains=value)
        )
    
    def group_filter(self, queryset, name, value):
        """Filter leads by user group ID"""
        return queryset.filter(
            Q(assigned_to__groups__id__in=value) |
            Q(created_by__groups__id__in=value)
        ).distinct()

    def active_filter(self, queryset, name, value):
        """Filter for active leads (not won, lost, or cancelled)"""
        if value:
            return queryset.exclude(status__in=['won', 'lost', 'cancelled'])
        return queryset.filter(status__in=['won', 'lost', 'cancelled'])