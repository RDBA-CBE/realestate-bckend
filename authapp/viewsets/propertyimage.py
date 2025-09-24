from rest_framework import viewsets
from common.paginator import Pagination
from ..models.propertyimage import PropertyImage
from ..serializers import (
    PropertyImageCreateSerializer,
    PropertyImageListSerializer,
    PropertyImageDetailSerializer,
    PropertyImageUpdateSerializer,
)

class PropertyImageViewSet(viewsets.ModelViewSet):
    queryset = PropertyImage.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete']
    pagination_class = Pagination

    def get_serializer_class(self):
        if self.action == "list":
            return PropertyImageListSerializer
        elif self.action == "retrieve":
            return PropertyImageDetailSerializer
        elif self.action == "create":
            return PropertyImageCreateSerializer
        elif self.action in ["update", "partial_update"]:
            return PropertyImageUpdateSerializer
        return PropertyImageDetailSerializer
