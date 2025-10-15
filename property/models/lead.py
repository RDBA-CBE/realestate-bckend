from django.db import models
from common.models import BaseModel
from django.contrib.auth import get_user_model
from .property import Property

CustomUser = get_user_model()


class Lead(BaseModel):
    LEAD_STATUS_CHOICES = [
        ('new', 'New'),
        ('contacted', 'Contacted'),
        ('qualified', 'Qualified'),
        ('proposal_sent', 'Proposal Sent'),
        ('negotiation', 'Negotiation'),
        ('won', 'Won'),
        ('lost', 'Lost'),
        ('cancelled', 'Cancelled'),
    ]

    LEAD_SOURCE_CHOICES = [
        ('website', 'Website'),
        ('referral', 'Referral'),
        ('social_media', 'Social Media'),
        ('advertisement', 'Advertisement'),
        ('cold_call', 'Cold Call'),
        ('email_campaign', 'Email Campaign'),
        ('walk_in', 'Walk In'),
        ('other', 'Other'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]

    # Lead Information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    alternate_phone = models.CharField(max_length=20, blank=True)

    # Property Interest
    interested_property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='leads'
    )
    budget_min = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Minimum budget"
    )
    budget_max = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Maximum budget"
    )
    preferred_location = models.CharField(
        max_length=255,
        blank=True,
        help_text="Preferred location/area"
    )
    requirements = models.TextField(
        blank=True,
        help_text="Specific requirements or notes"
    )

    # Lead Management
    status = models.CharField(
        max_length=20,
        choices=LEAD_STATUS_CHOICES,
        default='new'
    )
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='medium'
    )
    lead_source = models.CharField(
        max_length=20,
        choices=LEAD_SOURCE_CHOICES,
        default='website'
    )
    lead_source_details = models.CharField(
        max_length=255,
        blank=True,
        help_text="Additional details about the lead source"
    )

    # Assignment
    assigned_to = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_leads'
    )
    assigned_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='leads_assigned_by_me'
    )
    assigned_at = models.DateTimeField(null=True, blank=True)

    # Follow-up
    next_follow_up = models.DateTimeField(null=True, blank=True)
    last_contacted = models.DateTimeField(null=True, blank=True)
    contact_count = models.PositiveIntegerField(default=0)

    # Additional Information
    company_name = models.CharField(max_length=255, blank=True)
    occupation = models.CharField(max_length=100, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, default='India', blank=True)
    postal_code = models.CharField(max_length=20, blank=True)

    # Marketing
    newsletter_subscribed = models.BooleanField(default=False)
    sms_marketing = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Lead'
        verbose_name_plural = 'Leads'
        ordering = ['-created_at']
        unique_together = ('email', 'interested_property')
        indexes = [
            models.Index(fields=['status', 'priority']),
            models.Index(fields=['interested_property', 'status']),
            models.Index(fields=['assigned_to', 'status']),
            models.Index(fields=['email']),
            models.Index(fields=['phone']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.interested_property.title}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def is_active(self):
        return self.status not in ['won', 'lost', 'cancelled']

    @property
    def days_since_last_contact(self):
        if self.last_contacted:
            from django.utils import timezone
            return (timezone.now() - self.last_contacted).days
        return None

    @property
    def days_until_next_follow_up(self):
        if self.next_follow_up:
            from django.utils import timezone
            delta = self.next_follow_up - timezone.now()
            return delta.days if delta.days >= 0 else None
        return None

    def save(self, *args, **kwargs):
        # Update last_contacted when status changes to contacted or beyond
        if self.status in ['contacted', 'qualified', 'proposal_sent', 'negotiation', 'won', 'lost']:
            from django.utils import timezone
            if not self.last_contacted:
                self.last_contacted = timezone.now()
            self.contact_count += 1

        super().save(*args, **kwargs)