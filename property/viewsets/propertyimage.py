from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from common.paginator import Pagination
from ..models import PropertyImage
from ..filters.propertyimage import PropertyImageFilter
from ..serializers.propertyimage import (
    PropertyImageCreateSerializer,
    PropertyImageListSerializer,
    PropertyImageDetailSerializer,
    PropertyImageUpdateSerializer,
)

class PropertyImageViewSet(viewsets.ModelViewSet):
    queryset = PropertyImage.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete']
    filterset_class = PropertyImageFilter
    pagination_class = Pagination
    permission_classes = [IsAuthenticated]  # Add appropriate permissions

    def get_queryset(self):
        queryset = super().get_queryset()
        property_id = self.request.query_params.get('property', None)
        if property_id:
            queryset = queryset.filter(property_id=property_id)
        return queryset.order_by('order', 'created_at')

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
