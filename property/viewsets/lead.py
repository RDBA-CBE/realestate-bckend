from rest_framework import viewsets
from common.viewset import BaseViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Q
import django_filters
from common.paginator import Pagination
from ..models import Lead
from ..filters.lead import LeadFilter
from ..serializers.lead import (
    LeadListSerializer,
    LeadDetailSerializer,
    LeadCreateSerializer,
    LeadUpdateSerializer,
)


class LeadViewSet(BaseViewSet):
    queryset = Lead.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete']
    filterset_class = LeadFilter
    pagination_class = Pagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filter by property if specified
        property_id = self.request.query_params.get('property', None)
        if property_id:
            queryset = queryset.filter(interested_property_id=property_id)

        # Filter by assigned user if specified
        assigned_to = self.request.query_params.get('assigned_to', None)
        if assigned_to:
            queryset = queryset.filter(assigned_to_id=assigned_to)

        # Filter by current user's assigned leads if not admin/staff
        if not self.request.user.is_staff:
            queryset = queryset.filter(
                Q(assigned_to=self.request.user) |
                Q(interested_property__agent=self.request.user)
            )

        return queryset.order_by('-created_at')

    def get_serializer_class(self):
        if self.action == "list":
            return LeadListSerializer
        elif self.action == "retrieve":
            return LeadDetailSerializer
        elif self.action == "create":
            return LeadCreateSerializer
        elif self.action in ["update", "partial_update"]:
            return LeadUpdateSerializer
        return LeadDetailSerializer

    @action(detail=True, methods=['post'])
    def mark_contacted(self, request, pk=None):
        """Mark lead as contacted and update last_contacted timestamp"""
        lead = self.get_object()
        lead.status = 'contacted'
        lead.last_contacted = timezone.now()
        lead.contact_count += 1
        lead.save()

        serializer = self.get_serializer(lead)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def assign_to_me(self, request, pk=None):
        """Assign the lead to the current user"""
        lead = self.get_object()
        lead.assigned_to = request.user
        lead.assigned_by = request.user
        lead.assigned_at = timezone.now()
        lead.save()

        serializer = self.get_serializer(lead)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        """Update lead status"""
        lead = self.get_object()
        new_status = request.data.get('status')

        if new_status not in dict(Lead.LEAD_STATUS_CHOICES):
            return Response({'error': 'Invalid status'}, status=400)

        lead.status = new_status

        # Update last_contacted for certain statuses
        if new_status in ['contacted', 'qualified', 'proposal_sent', 'negotiation', 'won', 'lost']:
            lead.last_contacted = timezone.now()
            lead.contact_count += 1

        lead.save()

        serializer = self.get_serializer(lead)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get lead statistics"""
        queryset = self.get_queryset()

        stats = {
            'total_leads': queryset.count(),
            'new_leads': queryset.filter(status='new').count(),
            'contacted_leads': queryset.filter(status='contacted').count(),
            'qualified_leads': queryset.filter(status='qualified').count(),
            'won_leads': queryset.filter(status='won').count(),
            'lost_leads': queryset.filter(status='lost').count(),
            'active_leads': queryset.exclude(status__in=['won', 'lost', 'cancelled']).count(),
        }

        return Response(stats)

    @action(detail=False, methods=['get'])
    def overdue_followups(self, request):
        """Get leads with overdue follow-ups"""
        queryset = self.get_queryset().filter(
            next_follow_up__lt=timezone.now(),
            status__in=['new', 'contacted', 'qualified', 'proposal_sent', 'negotiation']
        )

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)