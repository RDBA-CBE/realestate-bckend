from django.db import models
from common.models import BaseModel
from authapp.models import CustomUser


class BuyerProfile(BaseModel):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="buyer_profile")
    
    # Personal Information
    date_of_birth = models.DateField(blank=True, null=True)
    phone_verified = models.BooleanField(default=False)
    
    # Real Estate Specific Info
    preferred_location = models.CharField(max_length=255, blank=True, null=True)
    budget_min = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    budget_max = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    interested_in_buying = models.BooleanField(default=False)
    interested_in_renting = models.BooleanField(default=False)
    
    # Preferences
    preferred_property_types = models.JSONField(default=list, blank=True)
    min_bedrooms = models.PositiveIntegerField(null=True, blank=True)
    preferred_amenities = models.JSONField(default=list, blank=True)
    
    # Communication preferences
    email_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=False)
    call_notifications = models.BooleanField(default=True)
    
    # Profile completion
    profile_completion_percentage = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.email}'s Buyer Profile"
    
    def is_profile_complete(self):
        """Check if buyer profile is complete"""
        required_fields = [
            self.user.first_name,
            self.user.last_name,
            self.user.phone,
            self.preferred_location,
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
        if self.preferred_location:
            completed_fields += 1
        if self.budget_min and self.budget_max:
            completed_fields += 1
        if self.date_of_birth:
            completed_fields += 1
        if self.interested_in_buying or self.interested_in_renting:
            completed_fields += 1
        if self.preferred_property_types:
            completed_fields += 1
        if self.min_bedrooms:
            completed_fields += 1
        if self.preferred_amenities:
            completed_fields += 1
        
        return int((completed_fields / total_fields) * 100)
    
    def save(self, *args, **kwargs):
        self.profile_completion_percentage = self.calculate_completion_percentage()
        super().save(*args, **kwargs)
    