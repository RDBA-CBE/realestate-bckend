import django_filters
from authapp.models.property import Property

class PropertyFilter(django_filters.FilterSet):
    class Meta:
        model = Property
        fields = ['city', 'status', 'property_type', 'price', 'project']
