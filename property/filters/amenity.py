import django_filters
from property.models import Amenity

class AmenityFilter(django_filters.FilterSet):
    class Meta:
        model = Amenity
        fields = "__all__"