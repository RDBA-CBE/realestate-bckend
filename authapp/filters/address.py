from django_filters import rest_framework as filters
from authapp.models import Address


class AddressFilter(filters.FilterSet):
    class Meta:
        model = Address
        fields = {
            "street": ["exact", "icontains"],
            "city": ["exact", "icontains"],
            "state": ["exact", "icontains"],
            "country": ["exact", "icontains"],
            "postal_code": ["exact", "icontains"],
        }
