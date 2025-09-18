from django_filters import rest_framework as filters
from authapp.models import CustomUser


class CustomUserFilter(filters.FilterSet):
    class Meta:
        model = CustomUser
        fields = {
            "email": ["exact", "icontains"],
            "phone": ["exact", "icontains"],
        }
