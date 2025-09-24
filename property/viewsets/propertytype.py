from rest_framework import viewsets
from common.paginator import Pagination
from ..models import PropertyType
from property.filters import PropertyTypeFilter
from ..serializers import (
    PropertyTypeListSerializer,
    PropertyTypeDetailSerializer,
    PropertyTypeCreateSerializer,
    PropertyTypeUpdateSerializer,
)

class PropertyTypeViewSet(viewsets.ModelViewSet):
    queryset = PropertyType.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete']
    filterset_class = PropertyTypeFilter
    pagination_class = Pagination

    def get_serializer_class(self):
        if self.action == "list":
            return PropertyTypeListSerializer
        elif self.action == "retrieve":
            return PropertyTypeDetailSerializer
        elif self.action == "create":
            return PropertyTypeCreateSerializer
        elif self.action in ["update", "partial_update"]:
            return PropertyTypeUpdateSerializer
        return PropertyTypeDetailSerializer