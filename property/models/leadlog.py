from django.db import models
from django.contrib.auth import get_user_model
from common.models import BaseModel
from .lead import Lead

CustomUser = get_user_model()


class LeadLog(BaseModel):
    """Simple model to track lead changes and activities"""
    
    ACTION_CHOICES = [
        ('created', 'Lead Created'),
        ('updated', 'Lead Updated'),
        ('status_changed', 'Status Changed'),
        ('assigned', 'Lead Assigned'),
        ('contacted', 'Lead Contacted'),
        ('note_added', 'Note Added'),
    ]

    # Core fields
    lead = models.ForeignKey(
        Lead,
        on_delete=models.CASCADE,
        related_name='logs'
    )
    action = models.CharField(
        max_length=20,
        choices=ACTION_CHOICES
    )
    performed_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='lead_actions_performed'
    )
    
    # Simple change tracking
    old_value = models.TextField(blank=True)
    new_value = models.TextField(blank=True)
    description = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    
    
    class Meta:
        verbose_name = 'Lead Log'
        verbose_name_plural = 'Lead Logs'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_action_display()} - {self.lead.full_name}"

    @classmethod
    def log_action(cls, lead, action, performed_by=None, old_value=None, new_value=None, description=None, notes=None):
        """Simple method to log any action"""
        return cls.objects.create(
            lead=lead,
            action=action,
            performed_by=performed_by,
            old_value=str(old_value) if old_value else '',
            new_value=str(new_value) if new_value else '',
            description=description or '',
            notes=notes or ''
        )