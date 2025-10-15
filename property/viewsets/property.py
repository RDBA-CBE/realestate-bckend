from rest_framework import viewsets
from common.viewset import BaseViewSet
from common.paginator import Pagination
from ..models import Property
from ..filters.property import PropertyFilter
from ..serializers.property import (
    PropertyListSerializer, 
    PropertyDetailSerializer,
    PropertyCreateSerializer,
    PropertyUpdateSerializer
)

class PropertyViewSet(BaseViewSet):
    queryset = Property.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete']
    filterset_class = PropertyFilter
    pagination_class = Pagination
    order_by = ['-id']  

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     # Only show approved properties to non-admin users
    #     if not self.request.user.groups.filter(name='Admin').exists():
    #         queryset = queryset.filter(is_approved=True)
    #     return queryset

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