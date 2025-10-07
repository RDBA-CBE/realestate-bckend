from django_filters import rest_framework as filters
from django.contrib.auth.models import Group
from authapp.models import CustomUser


class CustomUserFilter(filters.FilterSet):
    # Group filtering
    groups = filters.ModelMultipleChoiceFilter(
        queryset=Group.objects.all(),
        field_name='groups',
        to_field_name='name',
        help_text="Filter users by group names (e.g., 'Buyers', 'Sellers', 'Agents')"
    )
    
    # User type filtering (based on groups)
    user_type = filters.ChoiceFilter(
        choices=[
            ('admin', 'Admin'),
            ('developer', 'Developer'),
            ('agent', 'Agent'),
            ('seller', 'Seller'),
            ('buyer', 'Buyer'),
        ],
        method='filter_by_user_type',
        help_text="Filter by user type (based on group membership)"
    )
    
    # Account status filtering
    account_status = filters.ChoiceFilter(
        choices=CustomUser.ACCOUNT_STATUS_CHOICES,
        field_name='account_status'
    )
    
    # Email verification status
    is_email_verified = filters.BooleanFilter(
        field_name='is_email_verified'
    )
    
    # Active status
    is_active = filters.BooleanFilter(
        field_name='is_active'
    )
    
    # Date range filters
    created_after = filters.DateFilter(
        field_name='created_at',
        lookup_expr='gte'
    )
    created_before = filters.DateFilter(
        field_name='created_at',
        lookup_expr='lte'
    )
    
    class Meta:
        model = CustomUser
        fields = {
            "email": ["exact", "icontains"],
            "phone": ["exact", "icontains"],
            "first_name": ["exact", "icontains"],
            "last_name": ["exact", "icontains"],
        }
    
    def filter_by_user_type(self, queryset, name, value):
        """Custom filter method for user type based on group membership"""
        if value == 'admin':
            return queryset.filter(groups__name='Admins')
        elif value == 'developer':
            return queryset.filter(groups__name='Developers')
        elif value == 'agent':
            return queryset.filter(groups__name='Agents')
        elif value == 'seller':
            return queryset.filter(groups__name='Sellers')
        elif value == 'buyer':
            return queryset.filter(groups__name='Buyers')
        return queryset
