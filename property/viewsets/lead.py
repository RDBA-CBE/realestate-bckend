from rest_framework import viewsets
from common.viewset import BaseViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Q
import django_filters
from common.paginator import Pagination
from ..models import Lead, LeadLog
from ..filters.lead import LeadFilter
from ..serializers.lead import (
    LeadListSerializer,
    LeadDetailSerializer,
    LeadCreateSerializer,
    LeadUpdateSerializer,
)


class LeadViewSet(BaseViewSet):
    queryset = Lead.objects.all().order_by('-created_at')
    http_method_names = ['get', 'post', 'patch', 'delete']
    filterset_class = LeadFilter
    pagination_class = Pagination
    # permission_classes = [IsAuthenticated]

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

    def perform_create(self, serializer):
        """Create lead and log the creation"""
        lead = serializer.save()
        # Log the creation
        LeadLog.log_action(
            lead=lead,
            action='created',
            performed_by=self.request.user,
            description=f"Lead created for {lead.interested_property.title}"
        )

    def perform_update(self, serializer):
        """Update lead and log the changes"""
        # Get old values before update
        old_lead = Lead.objects.get(pk=serializer.instance.pk)
        old_status = old_lead.status
        old_assigned_to = old_lead.assigned_to
        
        # Save the updated lead
        lead = serializer.save()
        
        # Log status change if it changed
        if old_status != lead.status:
            LeadLog.log_action(
                lead=lead,
                action='status_changed',
                performed_by=self.request.user,
                old_value=old_status,
                new_value=lead.status,
                description=f"Status changed from '{old_status}' to '{lead.status}'"
            )
        
        # Log assignment change if it changed
        if old_assigned_to != lead.assigned_to:
            LeadLog.log_action(
                lead=lead,
                action='assigned',
                performed_by=self.request.user,
                old_value=str(old_assigned_to) if old_assigned_to else 'Unassigned',
                new_value=str(lead.assigned_to) if lead.assigned_to else 'Unassigned',
                description=f"Lead assigned to {lead.assigned_to.get_full_name() if lead.assigned_to else 'Unassigned'}"
            )
        
        # Log general update if no specific changes were tracked
        if old_status == lead.status and old_assigned_to == lead.assigned_to:
            LeadLog.log_action(
                lead=lead,
                action='updated',
                performed_by=self.request.user,
                description="Lead information updated"
            )

    @action(detail=True, methods=['post'])
    def mark_contacted(self, request, pk=None):
        """Mark lead as contacted and update last_contacted timestamp"""
        lead = self.get_object()
        old_status = lead.status
        
        lead.status = 'contacted'
        lead.last_contacted = timezone.now()
        lead.contact_count += 1
        lead.save()

        # Log the contact action
        LeadLog.log_action(
            lead=lead,
            action='contacted',
            performed_by=request.user,
            description=f"Lead contacted by {request.user.get_full_name()}"
        )

        serializer = self.get_serializer(lead)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def assign_to_me(self, request, pk=None):
        """Assign the lead to the current user"""
        lead = self.get_object()
        old_assigned_to = lead.assigned_to
        
        lead.assigned_to = request.user
        lead.assigned_by = request.user
        lead.assigned_at = timezone.now()
        lead.save()

        # Log the assignment
        LeadLog.log_action(
            lead=lead,
            action='assigned',
            performed_by=request.user,
            old_value=str(old_assigned_to) if old_assigned_to else 'Unassigned',
            new_value=str(request.user),
            description=f"Lead assigned to {request.user.get_full_name()}"
        )

        serializer = self.get_serializer(lead)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        """Update lead status"""
        lead = self.get_object()
        old_status = lead.status
        new_status = request.data.get('status')

        if new_status not in dict(Lead.LEAD_STATUS_CHOICES):
            return Response({'error': 'Invalid status'}, status=400)

        lead.status = new_status

        # Update last_contacted for certain statuses
        if new_status in ['contacted', 'qualified', 'proposal_sent', 'negotiation', 'won', 'lost']:
            lead.last_contacted = timezone.now()
            lead.contact_count += 1

        lead.save()

        # Log the status change
        LeadLog.log_action(
            lead=lead,
            action='status_changed',
            performed_by=request.user,
            old_value=old_status,
            new_value=new_status,
            description=f"Status changed from '{old_status}' to '{new_status}'"
        )

        serializer = self.get_serializer(lead)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def add_note(self, request, pk=None):
        """Add a note to the lead"""
        lead = self.get_object()
        note = request.data.get('note', '')
        
        if not note:
            return Response({'error': 'Note is required'}, status=400)

        # Log the note addition
        LeadLog.log_action(
            lead=lead,
            action='note_added',
            performed_by=request.user,
            description=f"Note added by {request.user.get_full_name()}",
            notes=note
        )

        return Response({'success': 'Note added successfully'})

    @action(detail=True, methods=['get'])
    def logs(self, request, pk=None):
        """Get logs for this specific lead"""
        lead = self.get_object()
        logs = LeadLog.objects.filter(lead=lead).order_by('-created_at')
        
        # Simple serialization
        logs_data = []
        for log in logs:
            logs_data.append({
                'id': log.id,
                'action': log.action,
                'action_display': log.get_action_display(),
                'performed_by': log.performed_by.get_full_name() if log.performed_by else 'System',
                'old_value': log.old_value,
                'new_value': log.new_value,
                'description': log.description,
                'notes': log.notes,
                'created_at': log.created_at
            })
        
        return Response(logs_data)

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