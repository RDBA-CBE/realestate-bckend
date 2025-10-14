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
    
    # Exclude specific user IDs
    exclude_users = filters.CharFilter(
        method='filter_exclude_users',
        help_text="Exclude specific user IDs (comma-separated string '1,2,3' or list [1,2,3])"
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
            return queryset.filter(groups__name='Admin')
        elif value == 'developer':
            return queryset.filter(groups__name='Developer')
        elif value == 'agent':
            return queryset.filter(groups__name='Agent')
        elif value == 'seller':
            return queryset.filter(groups__name='Seller')
        elif value == 'buyer':
            return queryset.filter(groups__name='Buyer')
        return queryset
    
    def filter_exclude_users(self, queryset, name, value):
        """Filter method to exclude specific user IDs"""
        if not value:
            return queryset
        
        # Handle both comma-separated string and list formats
        if isinstance(value, str):
            # Split comma-separated string and convert to integers
            try:
                user_ids_to_exclude = [int(id.strip()) for id in value.split(',') if id.strip()]
            except ValueError:
                # If conversion fails, return original queryset
                return queryset
        elif isinstance(value, list):
            # Handle list format directly
            try:
                user_ids_to_exclude = [int(id) for id in value if id is not None]
            except (ValueError, TypeError):
                # If conversion fails, return original queryset
                return queryset
        else:
            # Unsupported format, return original queryset
            return queryset
        
        return queryset.exclude(id__in=user_ids_to_exclude)
