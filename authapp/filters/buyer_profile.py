from django_filters import rest_framework as filters
from authapp.models import BuyerProfile


class BuyerProfileFilter(filters.FilterSet):
    class Meta:
        model = BuyerProfile
        fields = {
            "preferred_location": ["exact", "icontains"],
            "budget_min": ["exact", "gte", "lte"],
            "budget_max": ["exact", "gte", "lte"],
            "interested_in_buying": ["exact"],
            "interested_in_renting": ["exact"],
        }
