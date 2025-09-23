from django.db import models
from common.models import BaseModel
from authapp.models import CustomUser


class SellerProfile(BaseModel):
    VERIFICATION_STATUS_CHOICES = [
        ('pending', 'Pending Verification'),
        ('in_review', 'Under Review'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected'),
    ]
    
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="seller_profile")
    
    # Company Information (Optional)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    gst_number = models.CharField(max_length=30, blank=True, null=True)
    
    # Verification Documents
    identity_document = models.FileField(
        upload_to='seller_documents/identity/',
        blank=True,
        null=True,
        help_text="Aadhar/Passport/Driving License"
    )
    address_proof = models.FileField(
        upload_to='seller_documents/address/',
        blank=True,
        null=True,
        help_text="Utility bill/Bank statement"
    )
    property_ownership_proof = models.FileField(
        upload_to='seller_documents/ownership/',
        blank=True,
        null=True,
        help_text="Property documents/Title deeds"
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
        related_name='verified_sellers'
    )
    
    # Business Information
    years_in_business = models.PositiveIntegerField(null=True, blank=True)
    total_properties_sold = models.PositiveIntegerField(default=0)
    average_deal_value = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    
    # Contact Preferences
    preferred_contact_time = models.CharField(max_length=50, blank=True)
    available_days = models.JSONField(default=list, blank=True)
    
    # Profile completion
    profile_completion_percentage = models.PositiveIntegerField(default=0)
    documents_uploaded = models.BooleanField(default=False)

    def __str__(self):
        return f"Seller Profile: {self.user.email}"
    
    def is_profile_complete(self):
        """Check if seller profile is complete for approval"""
        required_fields = [
            self.user.first_name,
            self.user.last_name,
            self.user.phone,
            self.identity_document,
            self.address_proof,
        ]
        return all(field for field in required_fields)
    
    def calculate_completion_percentage(self):
        """Calculate profile completion percentage"""
        total_fields = 8
        completed_fields = 0
        
        # Check required fields
        if self.user.first_name:
            completed_fields += 1
        if self.user.last_name:
            completed_fields += 1
        if self.user.phone:
            completed_fields += 1
        if self.identity_document:
            completed_fields += 1
        if self.address_proof:
            completed_fields += 1
        if self.property_ownership_proof:
            completed_fields += 1
        if self.company_name or self.years_in_business:
            completed_fields += 1
        if self.preferred_contact_time:
            completed_fields += 1
        
        return int((completed_fields / total_fields) * 100)
    
    def save(self, *args, **kwargs):
        self.profile_completion_percentage = self.calculate_completion_percentage()
        
        # Check if documents are uploaded
        self.documents_uploaded = bool(
            self.identity_document and 
            self.address_proof
        )
        
        super().save(*args, **kwargs)