from django_filters import rest_framework as filters
from authapp.models import SellerProfile


class SellerProfileFilter(filters.FilterSet):
    class Meta:
        model = SellerProfile
        fields = {
            "company_name": ["exact", "icontains"],
            "gst_number": ["exact", "icontains"],
        }
