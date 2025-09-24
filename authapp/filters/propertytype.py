import django_filters
from authapp.models.property import PropertyType

class PropertyTypeFilter(django_filters.FilterSet):
    class Meta:
        model = PropertyType
        fields = ['name']
