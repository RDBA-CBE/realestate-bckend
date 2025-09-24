import django_filters
from authapp.models.property import Amenity

class AmenityFilter(django_filters.FilterSet):
    class Meta:
        model = Amenity
        fields = ['has_balcony', 'has_garden', 'has_swimming_pool', 'has_gym', 'has_elevator', 'has_security', 'has_power_backup', 'has_air_conditioning', 'pet_friendly']
