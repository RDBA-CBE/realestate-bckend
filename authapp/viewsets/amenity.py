from rest_framework import viewsets
from authapp.models.property import Amenity
from authapp.serializers.amenity import (
    AmenityListSerializer,
    AmenityDetailSerializer,
    AmenityCreateSerializer,
    AmenityUpdateSerializer
)

class AmenityViewSet(viewsets.ModelViewSet):
    queryset = Amenity.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.action == "list":
            return AmenityListSerializer
        elif self.action == "retrieve":
            return AmenityDetailSerializer
        elif self.action == "create":
            return AmenityCreateSerializer
        elif self.action in ["update", "partial_update"]:
            return AmenityUpdateSerializer
        return AmenityDetailSerializer
