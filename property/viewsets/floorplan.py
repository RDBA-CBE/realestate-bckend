from rest_framework import viewsets
from common.viewset import BaseViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from common.paginator import Pagination
from ..models import FloorPlan
from ..filters.floorplan import FloorPlanFilter
from ..serializers.floorplan import (
    FloorPlanListSerializer,
    FloorPlanDetailSerializer,
    FloorPlanCreateSerializer,
    FloorPlanUpdateSerializer,
    FloorPlanBulkCreateSerializer,
    FloorPlanBulkUpdateSerializer,
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
            return FloorPlanBulkCreateSerializer
        elif self.action in ["update", "partial_update"]:
            return FloorPlanUpdateSerializer
        return FloorPlanDetailSerializer

    @action(detail=False, methods=['post'], url_path='bulk-create')
    def bulk_create(self, request):
        """Create multiple floor plans at once"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            floor_plans = serializer.save()
            response_serializer = FloorPlanListSerializer(floor_plans, many=True, context={'request': request})
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['patch'], url_path='bulk-update')
    def bulk_update(self, request):
        """Update multiple floor plans at once"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            floor_plans = serializer.update(None, serializer.validated_data)
            response_serializer = FloorPlanListSerializer(floor_plans, many=True, context={'request': request})
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)