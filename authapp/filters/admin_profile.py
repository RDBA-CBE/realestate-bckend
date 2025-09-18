from django_filters import rest_framework as filters
from authapp.models import AdminProfile


class AdminProfileFilter(filters.FilterSet):
    class Meta:
        model = AdminProfile
        fields = {
            "department": ["exact", "icontains"],
            "designation": ["exact", "icontains"],
        }
