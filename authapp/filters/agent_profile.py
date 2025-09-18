from django_filters import rest_framework as filters
from authapp.models import AgentProfile


class AgentProfileFilter(filters.FilterSet):
    class Meta:
        model = AgentProfile
        fields = {
            "license_number": ["exact", "icontains"],
            "experience_years": ["exact", "gte", "lte"],
        }
