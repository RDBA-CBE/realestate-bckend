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

    @action(detail=False, methods=['get'])
    def by_lead(self, request):
        """Get logs for a specific lead"""
        lead_id = request.query_params.get('lead_id')
        if not lead_id:
            return Response(
                {"error": "lead_id parameter is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        queryset = self.queryset.filter(lead_id=lead_id)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Get recent logs (last 50)"""
        queryset = self.queryset[:50]
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get simple log statistics"""
        from django.db.models import Count
        from django.utils import timezone
        from datetime import timedelta
        
        stats = {
            'total_logs': self.queryset.count(),
            'actions_breakdown': dict(
                self.queryset.values('action')
                .annotate(count=Count('action'))
                .values_list('action', 'count')
            ),
            'recent_count': self.queryset.filter(
                created_at__gte=timezone.now() - timedelta(days=7)
            ).count()
        }
        
        return Response(stats)