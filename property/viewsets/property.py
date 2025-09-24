from rest_framework import viewsets
from common.paginator import Pagination
from ..models import Property
from property.filters import PropertyFilter
from ..serializers import (
    PropertyListSerializer, 
    PropertyDetailSerializer,
    PropertyCreateSerializer,
    PropertyUpdateSerializer
)

class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete']
    filterset_class = PropertyFilter
    pagination_class = Pagination
    order_by = ['-id']  

    def get_serializer_class(self):
        if self.action == "list":
            return PropertyListSerializer
        elif self.action == "retrieve":
            return PropertyDetailSerializer
        elif self.action == "create":
            return PropertyCreateSerializer
        elif self.action in ["update", "partial_update"]:
            return PropertyUpdateSerializer
        return PropertyDetailSerializer