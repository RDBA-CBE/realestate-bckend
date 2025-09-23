from django.db import models
from common.models import BaseModel
from authapp.models import CustomUser


class DeveloperProfile(BaseModel):
    VERIFICATION_STATUS_CHOICES = [
        ('pending', 'Pending Verification'),
        ('in_review', 'Under Review'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected'),
    ]
    
    COMPANY_TYPE_CHOICES = [
        ('individual', 'Individual Developer'),
        ('partnership', 'Partnership Firm'),
        ('private_limited', 'Private Limited Company'),
        ('public_limited', 'Public Limited Company'),
        ('llp', 'Limited Liability Partnership'),
    ]
    
    user = models.OneToOneField(
        CustomUser, 
        on_delete=models.CASCADE, 
        related_name="developer_profile"
    )
    
    # Company Information
    company_name = models.CharField(max_length=255)
    company_type = models.CharField(
        max_length=20,
        choices=COMPANY_TYPE_CHOICES,
        default='private_limited'
    )
    registration_number = models.CharField(max_length=50, unique=True)
    established_year = models.PositiveIntegerField()
    
    # Contact Information
    company_address = models.TextField()
    company_phone = models.CharField(max_length=15)
    company_email = models.EmailField()
    website = models.URLField(blank=True, null=True)
    
    # Financial Information
    annual_turnover = models.DecimalField(
        max_digits=15, 
        decimal_places=2, 
        null=True, 
        blank=True
    )
    pan_number = models.CharField(max_length=10, unique=True)
    gst_number = models.CharField(max_length=15, unique=True)
    
    # Verification Documents
    company_registration_certificate = models.FileField(
        upload_to='developer_documents/registration/',
        blank=True,
        null=True
    )
    pan_card = models.FileField(
        upload_to='developer_documents/pan/',
        blank=True,
        null=True
    )
    gst_certificate = models.FileField(
        upload_to='developer_documents/gst/',
        blank=True,
        null=True
    )
    financial_statements = models.FileField(
        upload_to='developer_documents/financial/',
        blank=True,
        null=True,
        help_text="Last 3 years financial statements"
    )
    rera_registration = models.FileField(
        upload_to='developer_documents/rera/',
        blank=True,
        null=True,
        help_text="RERA registration certificate"
    )
    
    # Portfolio Information
    total_projects_completed = models.PositiveIntegerField(default=0)
    total_units_delivered = models.PositiveIntegerField(default=0)
    ongoing_projects = models.PositiveIntegerField(default=0)
    
    # Specialization
    project_types = models.JSONField(
        default=list,
        help_text="Types of projects (residential, commercial, industrial, etc.)"
    )
    service_locations = models.JSONField(
        default=list,
        help_text="Cities/regions where developer operates"
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
        related_name='verified_developers'
    )
    
    # Rating and Reviews
    average_rating = models.DecimalField(
        max_digits=3, 
        decimal_places=2, 
        default=0.00
    )
    total_reviews = models.PositiveIntegerField(default=0)
    
    # Profile completion
    profile_completion_percentage = models.PositiveIntegerField(default=0)
    documents_uploaded = models.BooleanField(default=False)

    def __str__(self):
        return f"Developer Profile: {self.company_name}"
    
    def is_profile_complete(self):
        """Check if developer profile is complete for approval"""
        required_fields = [
            self.company_name,
            self.registration_number,
            self.established_year,
            self.company_address,
            self.company_phone,
            self.pan_number,
            self.gst_number,
            self.company_registration_certificate,
            self.pan_card,
            self.gst_certificate,
        ]
        return all(field for field in required_fields)
    
    def calculate_completion_percentage(self):
        """Calculate profile completion percentage"""
        total_fields = 12
        completed_fields = 0
        
        # Check required fields
        if self.company_name:
            completed_fields += 1
        if self.registration_number:
            completed_fields += 1
        if self.established_year:
            completed_fields += 1
        if self.company_address:
            completed_fields += 1
        if self.company_phone:
            completed_fields += 1
        if self.pan_number:
            completed_fields += 1
        if self.gst_number:
            completed_fields += 1
        if self.company_registration_certificate:
            completed_fields += 1
        if self.pan_card:
            completed_fields += 1
        if self.gst_certificate:
            completed_fields += 1
        if self.project_types:
            completed_fields += 1
        if self.service_locations:
            completed_fields += 1
        
        return int((completed_fields / total_fields) * 100)
    
    @property
    def years_in_business(self):
        """Calculate years in business"""
        from datetime import datetime
        current_year = datetime.now().year
        return current_year - self.established_year
    
    def save(self, *args, **kwargs):
        self.profile_completion_percentage = self.calculate_completion_percentage()
        
        # Check if minimum documents are uploaded
        self.documents_uploaded = bool(
            self.company_registration_certificate and 
            self.pan_card and 
            self.gst_certificate
        )
        
        super().save(*args, **kwargs)