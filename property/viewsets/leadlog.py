from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from common.paginator import Pagination
from common.viewset import BaseViewSet
from ..models import LeadLog
from ..filters.leadlog import LeadLogFilter
from ..serializers.leadlog import (
    LeadLogListSerializer,
    LeadLogDetailSerializer,
    LeadLogCreateSerializer
)


class LeadLogViewSet(BaseViewSet):
    """Simple ViewSet for managing lead logs"""
    queryset = LeadLog.objects.all().order_by('-created_at')
    http_method_names = ['get', 'post']
    filterset_class = LeadLogFilter
    pagination_class = Pagination
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "list":
            return LeadLogListSerializer
        elif self.action == "retrieve":
            return LeadLogDetailSerializer
        elif self.action == "create":
            return LeadLogCreateSerializer
        return LeadLogDetailSerializer

    def list(self, request, *args, **kwargs):
        """List lead logs with optional pagination"""
        # Check pagination parameter
        use_pagination = request.query_params.get('pagination', 'true').lower() == 'true'
        
        queryset = self.filter_queryset(self.get_queryset())
        
        if use_pagination:
            # Use pagination
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
        
        # No pagination - return all results
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    