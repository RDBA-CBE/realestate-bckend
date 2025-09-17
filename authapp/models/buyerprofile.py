from django.db import models
from common.models import BaseModel
from authapp.models import CustomUser


class BuyerProfile(BaseModel):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="profile")
    date_of_birth = models.DateField(blank=True, null=True)
    # Real Estate Specific Info
    preferred_location = models.CharField(max_length=255, blank=True, null=True)
    budget_min = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    budget_max = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    interested_in_buying = models.BooleanField(default=False)
    interested_in_renting = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s Profile"
    