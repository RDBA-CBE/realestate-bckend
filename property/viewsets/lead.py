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
        
        # Call parent create to save the instance
        super().perform_create(serializer)
        lead = serializer.instance  # instance is now available

        # Determine who performed the action
        performed_by = self.request.user if self.request.user.is_authenticated else None

        # Log creation
        LeadLog.log_action(
            lead=lead,
            action='created',
            performed_by=performed_by,
            description=f"Lead created for {lead.interested_property.title}"
        )

    def perform_update(self, serializer):
        """Update lead and log the changes"""
        # Capture old values before update
        old_lead = Lead.objects.get(pk=serializer.instance.pk)
        old_status = old_lead.status
        old_assigned_to = old_lead.assigned_to
        
        # Capture all important fields that can be updated
        old_values = {
            'first_name': old_lead.first_name,
            'last_name': old_lead.last_name,
            'email': old_lead.email,
            'phone': old_lead.phone,
            'alternate_phone': old_lead.alternate_phone,
            'budget_min': str(old_lead.budget_min) if old_lead.budget_min else '',
            'budget_max': str(old_lead.budget_max) if old_lead.budget_max else '',
            'preferred_location': old_lead.preferred_location,
            'requirements': old_lead.requirements,
            'priority': old_lead.priority,
            'lead_source': old_lead.lead_source,
            'lead_source_details': old_lead.lead_source_details,
            'next_follow_up': str(old_lead.next_follow_up) if old_lead.next_follow_up else '',
            'company_name': old_lead.company_name,
            'occupation': old_lead.occupation,
            'address': old_lead.address,
            'city': old_lead.city,
            'state': old_lead.state,
            'country': old_lead.country,
            'postal_code': old_lead.postal_code,
            'newsletter_subscribed': str(old_lead.newsletter_subscribed),
            'sms_marketing': str(old_lead.sms_marketing),
        }

        # Perform the update using parent method
        super().perform_update(serializer)
        lead = serializer.instance

        # Determine who performed the action
        performed_by = self.request.user if self.request.user.is_authenticated else None

        # Track what changed
        changes = []
        
        # Check status change
        if old_status != lead.status:
            changes.append(f"Status: '{old_status}' → '{lead.status}'")
            LeadLog.log_action(
                lead=lead,
                action='status_changed',
                performed_by=performed_by,
                old_value=old_status,
                new_value=lead.status,
                description=f"Status changed from '{old_status}' to '{lead.status}'"
            )

        # Check assignment change
        if old_assigned_to != lead.assigned_to:
            old_assigned_name = str(old_assigned_to) if old_assigned_to else 'Unassigned'
            new_assigned_name = str(lead.assigned_to) if lead.assigned_to else 'Unassigned'
            changes.append(f"Assigned to: '{old_assigned_name}' → '{new_assigned_name}'")
            LeadLog.log_action(
                lead=lead,
                action='assigned',
                performed_by=performed_by,
                old_value=old_assigned_name,
                new_value=new_assigned_name,
                description=f"Lead assigned to {new_assigned_name}"
            )

        # Check other field changes
        field_changes = []
        if old_values['first_name'] != lead.first_name:
            field_changes.append(f"First name: '{old_values['first_name']}' → '{lead.first_name}'")
        if old_values['last_name'] != lead.last_name:
            field_changes.append(f"Last name: '{old_values['last_name']}' → '{lead.last_name}'")
        if old_values['email'] != lead.email:
            field_changes.append(f"Email: '{old_values['email']}' → '{lead.email}'")
        if old_values['phone'] != lead.phone:
            field_changes.append(f"Phone: '{old_values['phone']}' → '{lead.phone}'")
        if old_values['alternate_phone'] != lead.alternate_phone:
            field_changes.append(f"Alternate phone: '{old_values['alternate_phone']}' → '{lead.alternate_phone}'")
        if old_values['budget_min'] != (str(lead.budget_min) if lead.budget_min else ''):
            field_changes.append(f"Min budget: '{old_values['budget_min']}' → '{lead.budget_min}'")
        if old_values['budget_max'] != (str(lead.budget_max) if lead.budget_max else ''):
            field_changes.append(f"Max budget: '{old_values['budget_max']}' → '{lead.budget_max}'")
        if old_values['preferred_location'] != lead.preferred_location:
            field_changes.append(f"Preferred location: '{old_values['preferred_location']}' → '{lead.preferred_location}'")
        if old_values['requirements'] != lead.requirements:
            field_changes.append(f"Requirements: '{old_values['requirements']}' → '{lead.requirements}'")
        if old_values['priority'] != lead.priority:
            field_changes.append(f"Priority: '{old_values['priority']}' → '{lead.priority}'")
        if old_values['lead_source'] != lead.lead_source:
            field_changes.append(f"Lead source: '{old_values['lead_source']}' → '{lead.lead_source}'")
        if old_values['lead_source_details'] != lead.lead_source_details:
            field_changes.append(f"Lead source details: '{old_values['lead_source_details']}' → '{lead.lead_source_details}'")
        if old_values['next_follow_up'] != (str(lead.next_follow_up) if lead.next_follow_up else ''):
            field_changes.append(f"Next follow up: '{old_values['next_follow_up']}' → '{lead.next_follow_up}'")
        if old_values['company_name'] != lead.company_name:
            field_changes.append(f"Company: '{old_values['company_name']}' → '{lead.company_name}'")
        if old_values['occupation'] != lead.occupation:
            field_changes.append(f"Occupation: '{old_values['occupation']}' → '{lead.occupation}'")
        if old_values['address'] != lead.address:
            field_changes.append(f"Address: '{old_values['address']}' → '{lead.address}'")
        if old_values['city'] != lead.city:
            field_changes.append(f"City: '{old_values['city']}' → '{lead.city}'")
        if old_values['state'] != lead.state:
            field_changes.append(f"State: '{old_values['state']}' → '{lead.state}'")
        if old_values['country'] != lead.country:
            field_changes.append(f"Country: '{old_values['country']}' → '{lead.country}'")
        if old_values['postal_code'] != lead.postal_code:
            field_changes.append(f"Postal code: '{old_values['postal_code']}' → '{lead.postal_code}'")
        if old_values['newsletter_subscribed'] != str(lead.newsletter_subscribed):
            field_changes.append(f"Newsletter: '{old_values['newsletter_subscribed']}' → '{lead.newsletter_subscribed}'")
        if old_values['sms_marketing'] != str(lead.sms_marketing):
            field_changes.append(f"SMS marketing: '{old_values['sms_marketing']}' → '{lead.sms_marketing}'")

        # Log general update with all changes
        if field_changes or (not changes):  # Log if there are field changes or if no status/assignment changes
            all_changes = changes + field_changes
            change_summary = "; ".join(all_changes) if all_changes else "Lead information updated"
            
            LeadLog.log_action(
                lead=lead,
                action='updated',
                performed_by=performed_by,
                old_value="; ".join([f"{k}: {v}" for k, v in old_values.items() if v]),
                new_value="; ".join([
                    f"first_name: {lead.first_name}",
                    f"last_name: {lead.last_name}", 
                    f"email: {lead.email}",
                    f"phone: {lead.phone}",
                    f"alternate_phone: {lead.alternate_phone}",
                    f"budget_min: {lead.budget_min}",
                    f"budget_max: {lead.budget_max}",
                    f"preferred_location: {lead.preferred_location}",
                    f"requirements: {lead.requirements}",
                    f"priority: {lead.priority}",
                    f"lead_source: {lead.lead_source}",
                    f"lead_source_details: {lead.lead_source_details}",
                    f"next_follow_up: {lead.next_follow_up}",
                    f"company_name: {lead.company_name}",
                    f"occupation: {lead.occupation}",
                    f"address: {lead.address}",
                    f"city: {lead.city}",
                    f"state: {lead.state}",
                    f"country: {lead.country}",
                    f"postal_code: {lead.postal_code}",
                    f"newsletter_subscribed: {lead.newsletter_subscribed}",
                    f"sms_marketing: {lead.sms_marketing}"
                ]),
                description=change_summary
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
        performed_by = request.user if request.user.is_authenticated else None
        LeadLog.log_action(
            lead=lead,
            action='contacted',
            performed_by=performed_by,
            description=f"Lead contacted by {request.user.get_full_name() if performed_by else 'Anonymous user'}"
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
        performed_by = request.user if request.user.is_authenticated else None
        LeadLog.log_action(
            lead=lead,
            action='assigned',
            performed_by=performed_by,
            old_value=str(old_assigned_to) if old_assigned_to else 'Unassigned',
            new_value=str(request.user) if performed_by else 'Unknown',
            description=f"Lead assigned to {request.user.get_full_name() if performed_by else 'Unknown user'}"
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
        performed_by = request.user if request.user.is_authenticated else None
        LeadLog.log_action(
            lead=lead,
            action='status_changed',
            performed_by=performed_by,
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
        performed_by = request.user if request.user.is_authenticated else None
        LeadLog.log_action(
            lead=lead,
            action='note_added',
            performed_by=performed_by,
            description=f"Note added by {request.user.get_full_name() if performed_by else 'Anonymous user'}",
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
                'performed_by': log.performed_by.get_full_name() if log.performed_by else 'Anonymous User',
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