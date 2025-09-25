from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from common.paginator import Pagination
from ..models import VirtualTour
from ..serializers.virtualtour import (
    VirtualTourListSerializer,
    VirtualTourDetailSerializer,
    VirtualTourCreateSerializer,
    VirtualTourUpdateSerializer,
)

class VirtualTourViewSet(viewsets.ModelViewSet):
    queryset = VirtualTour.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete']
    pagination_class = Pagination
    permission_classes = [IsAuthenticated]  # Add appropriate permissions

    def get_queryset(self):
        queryset = super().get_queryset()
        property_id = self.request.query_params.get('property', None)
        if property_id:
            queryset = queryset.filter(property_id=property_id)
        # Only return active tours by default
        show_inactive = self.request.query_params.get('show_inactive', 'false').lower() == 'true'
        if not show_inactive:
            queryset = queryset.filter(is_active=True)
        return queryset.order_by('order', 'created_at')

    def get_serializer_class(self):
        if self.action == "list":
            return VirtualTourListSerializer
        elif self.action == "retrieve":
            return VirtualTourDetailSerializer
        elif self.action == "create":
            return VirtualTourCreateSerializer
        elif self.action in ["update", "partial_update"]:
            return VirtualTourUpdateSerializer
        return VirtualTourDetailSerializer