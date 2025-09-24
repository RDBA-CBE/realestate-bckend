from django.db import models
from django.core.validators import RegexValidator
from common.models import BaseModel
from .property import Property
from authapp.models import CustomUser


class PropertyInquiry(BaseModel):
    INQUIRY_TYPE_CHOICES = [
        ('general', 'General Inquiry'),
        ('viewing', 'Schedule Viewing'),
        ('purchase', 'Purchase Intent'),
        ('rental', 'Rental Inquiry'),
        ('more_info', 'More Information'),
        ('price_negotiation', 'Price Negotiation'),
        ('callback', 'Request Callback'),
    ]

    STATUS_CHOICES = [
        ('new', 'New'),
        ('contacted', 'Contacted'),
        ('in_progress', 'In Progress'),
        ('viewing_scheduled', 'Viewing Scheduled'),
        ('closed', 'Closed'),
        ('spam', 'Spam'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]

    property_obj = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='inquiries'
    )
    inquirer = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='inquiries_made',
        null=True,
        blank=True
    )
    
    # Contact Information (for non-registered users)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be in format: '+999999999'. Up to 15 digits allowed."
    )
    phone = models.CharField(validators=[phone_regex], max_length=17)
    
    # Inquiry Details
    inquiry_type = models.CharField(max_length=20, choices=INQUIRY_TYPE_CHOICES)
    message = models.TextField()
    budget = models.DecimalField(
        max_digits=15, 
        decimal_places=2, 
        null=True, 
        blank=True,
        help_text="Inquirer's budget if applicable"
    )
    preferred_viewing_date = models.DateTimeField(null=True, blank=True)
    
    # Status and Management
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    assigned_to = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_inquiries',
        help_text="Agent/Admin assigned to handle this inquiry"
    )
    
    # Response Details
    response_message = models.TextField(blank=True)
    responded_at = models.DateTimeField(null=True, blank=True)
    responded_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='inquiries_responded'
    )
    
    # Follow-up
    follow_up_date = models.DateTimeField(null=True, blank=True)
    follow_up_notes = models.TextField(blank=True)
    
    # Tracking
    source = models.CharField(
        max_length=50, 
        blank=True,
        help_text="Source of inquiry (website, mobile app, etc.)"
    )
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Property Inquiry'
        verbose_name_plural = 'Property Inquiries'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'created_at']),
            models.Index(fields=['property_obj', 'status']),
            models.Index(fields=['assigned_to', 'status']),
        ]

    def __str__(self):
        return f"Inquiry from {self.name} for {self.property_obj.title}"

    @property
    def is_overdue(self):
        """Check if inquiry is overdue for response (more than 24 hours old and new)"""
        if self.status == 'new':
            from django.utils import timezone
            from datetime import timedelta
            return timezone.now() - self.created_at > timedelta(hours=24)
        return False

    @property
    def days_since_inquiry(self):
        """Number of days since inquiry was made"""
        from django.utils import timezone
        return (timezone.now().date() - self.created_at.date()).days


class PropertyViewing(BaseModel):
    """Model to track property viewing appointments"""
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
        ('rescheduled', 'Rescheduled'),
    ]

    inquiry = models.ForeignKey(
        PropertyInquiry,
        on_delete=models.CASCADE,
        related_name='viewings'
    )
    property_obj = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='viewings'
    )
    viewer = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='property_viewings',
        null=True,
        blank=True
    )
    
    # Viewing Details
    scheduled_date = models.DateTimeField()
    actual_date = models.DateTimeField(null=True, blank=True)
    duration_minutes = models.PositiveIntegerField(default=30)
    
    # Contact Information
    viewer_name = models.CharField(max_length=100)
    viewer_email = models.EmailField()
    viewer_phone = models.CharField(max_length=17)
    
    # Management
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='scheduled')
    conducted_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='conducted_viewings',
        help_text="Agent who conducted the viewing"
    )
    
    # Feedback
    viewer_feedback = models.TextField(blank=True)
    agent_notes = models.TextField(blank=True)
    interested_level = models.PositiveIntegerField(
        null=True,
        blank=True,
        choices=[(i, i) for i in range(1, 6)],
        help_text="Interest level from 1-5"
    )
    
    # Follow-up
    follow_up_required = models.BooleanField(default=False)
    next_action = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name = 'Property Viewing'
        verbose_name_plural = 'Property Viewings'
        ordering = ['-scheduled_date']

    def __str__(self):
        return f"Viewing: {self.property_obj.title} by {self.viewer_name} on {self.scheduled_date.date()}"

    @property
    def is_upcoming(self):
        """Check if viewing is in the future"""
        from django.utils import timezone
        return self.scheduled_date > timezone.now()

    @property
    def is_today(self):
        """Check if viewing is today"""
        from django.utils import timezone
        return self.scheduled_date.date() == timezone.now().date()