import django_filters
from ..models import Amenity

class AmenityFilter(django_filters.FilterSet):
    class Meta:
        model = Amenity
        fields = ['name', 'category', 'is_active']