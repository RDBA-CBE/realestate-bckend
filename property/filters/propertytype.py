import django_filters
from property.models import PropertyType

class PropertyTypeFilter(django_filters.FilterSet):
    class Meta:
        model = PropertyType
        fields = ['name']
