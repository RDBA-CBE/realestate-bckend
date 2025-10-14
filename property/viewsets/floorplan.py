from rest_framework import viewsets
from common.viewset import BaseViewSet
from rest_framework.permissions import IsAuthenticated
from common.paginator import Pagination
from ..models import FloorPlan
from ..filters.floorplan import FloorPlanFilter
from ..serializers.floorplan import (
    FloorPlanListSerializer,
    FloorPlanDetailSerializer,
    FloorPlanCreateSerializer,
    FloorPlanUpdateSerializer,
)


class FloorPlanViewSet(BaseViewSet):
    queryset = FloorPlan.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete']
    filterset_class = FloorPlanFilter
    pagination_class = Pagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        property_id = self.request.query_params.get('property', None)
        if property_id:
            queryset = queryset.filter(property_id=property_id)

        # Only show floor plans of approved properties to non-admin users
        if not self.request.user.groups.filter(name='Admin').exists():
            queryset = queryset.filter(property__is_approved=True)

        return queryset.order_by('category', 'square_feet')

    def get_serializer_class(self):
        if self.action == "list":
            return FloorPlanListSerializer
        elif self.action == "retrieve":
            return FloorPlanDetailSerializer
        elif self.action == "create":
            return FloorPlanCreateSerializer
        elif self.action in ["update", "partial_update"]:
            return FloorPlanUpdateSerializer
        return FloorPlanDetailSerializer