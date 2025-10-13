from rest_framework import viewsets
from common.viewset import BaseViewSet
from rest_framework.permissions import IsAuthenticated
from common.paginator import Pagination
from ..models import PropertyVideo
from ..filters.propertyvideo import PropertyVideoFilter
from ..serializers.propertyvideo import (
    PropertyVideoListSerializer,
    PropertyVideoDetailSerializer,
    PropertyVideoCreateSerializer,
    PropertyVideoUpdateSerializer,
)

class PropertyVideoViewSet(BaseViewSet):
    queryset = PropertyVideo.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete']
    filterset_class = PropertyVideoFilter
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
            return PropertyVideoListSerializer
        elif self.action == "retrieve":
            return PropertyVideoDetailSerializer
        elif self.action == "create":
            return PropertyVideoCreateSerializer
        elif self.action in ["update", "partial_update"]:
            return PropertyVideoUpdateSerializer
        return PropertyVideoDetailSerializer