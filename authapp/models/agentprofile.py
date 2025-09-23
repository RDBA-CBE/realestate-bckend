# models.py
from django.db import models
from common.models import BaseModel
from authapp.models import CustomUser

class AgentProfile(BaseModel):
    VERIFICATION_STATUS_CHOICES = [
        ('pending', 'Pending Verification'),
        ('in_review', 'Under Review'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected'),
    ]
    
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, 
        related_name="agent_profile"
    )
    
    # Professional Information
    license_number = models.CharField(max_length=50)
    experience_years = models.IntegerField(default=0)
    specialization = models.JSONField(
        default=list,
        help_text="Areas of specialization (residential, commercial, etc.)"
    )
    
    # Agency Information
    agency_name = models.CharField(max_length=255, blank=True, null=True)
    agency_address = models.TextField(blank=True, null=True)
    agency_phone = models.CharField(max_length=15, blank=True, null=True)
    commission_rate = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        null=True, 
        blank=True,
        help_text="Commission rate in percentage"
    )
    
    # Verification Documents
    license_document = models.FileField(
        upload_to='agent_documents/license/',
        blank=True,
        null=True,
        help_text="Real estate license document"
    )
    identity_document = models.FileField(
        upload_to='agent_documents/identity/',
        blank=True,
        null=True,
        help_text="Government issued ID"
    )
    agency_authorization = models.FileField(
        upload_to='agent_documents/authorization/',
        blank=True,
        null=True,
        help_text="Agency authorization letter"
    )
    
    # Verification Status
    verification_status = models.CharField(
        max_length=20,
        choices=VERIFICATION_STATUS_CHOICES,
        default='pending'
    )
    verification_notes = models.TextField(blank=True, null=True)
    verified_at = models.DateTimeField(null=True, blank=True)
    verified_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='verified_agents'
    )
    
    # Performance Metrics
    total_listings = models.PositiveIntegerField(default=0)
    successful_deals = models.PositiveIntegerField(default=0)
    client_rating = models.DecimalField(
        max_digits=3, 
        decimal_places=2, 
        default=0.00,
        help_text="Average client rating out of 5"
    )
    
    # Working Areas
    service_areas = models.JSONField(
        default=list,
        help_text="List of cities/areas where agent provides service"
    )
    
    # Contact Preferences
    available_hours = models.CharField(max_length=100, blank=True)
    preferred_contact_method = models.CharField(
        max_length=20,
        choices=[
            ('phone', 'Phone'),
            ('email', 'Email'),
            ('whatsapp', 'WhatsApp'),
            ('any', 'Any Method')
        ],
        default='phone'
    )
    
    # Profile completion
    profile_completion_percentage = models.PositiveIntegerField(default=0)
    documents_uploaded = models.BooleanField(default=False)

    def __str__(self):
        return f"Agent Profile: {self.user.email}"
    
    def is_profile_complete(self):
        """Check if agent profile is complete for approval"""
        required_fields = [
            self.user.first_name,
            self.user.last_name,
            self.user.phone,
            self.license_number,
            self.license_document,
            self.identity_document,
            self.agency_name,
        ]
        return all(field for field in required_fields)
    
    def calculate_completion_percentage(self):
        """Calculate profile completion percentage"""
        total_fields = 10
        completed_fields = 0
        
        # Check required fields
        if self.user.first_name:
            completed_fields += 1
        if self.user.last_name:
            completed_fields += 1
        if self.user.phone:
            completed_fields += 1
        if self.license_number:
            completed_fields += 1
        if self.license_document:
            completed_fields += 1
        if self.identity_document:
            completed_fields += 1
        if self.agency_name:
            completed_fields += 1
        if self.experience_years:
            completed_fields += 1
        if self.specialization:
            completed_fields += 1
        if self.service_areas:
            completed_fields += 1
        
        return int((completed_fields / total_fields) * 100)
    
    @property
    def success_rate(self):
        """Calculate success rate as percentage of successful deals"""
        if self.total_listings == 0:
            return 0
        return round((self.successful_deals / self.total_listings) * 100, 2)
    
    def save(self, *args, **kwargs):
        self.profile_completion_percentage = self.calculate_completion_percentage()
        
        # Check if documents are uploaded
        self.documents_uploaded = bool(
            self.license_document and 
            self.identity_document
        )
        
        super().save(*args, **kwargs)