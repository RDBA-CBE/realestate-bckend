from django.db import models
from common.models import BaseModel
from models import CustomUser


class SellerProfile(BaseModel):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="seller_profile")
    company_name = models.CharField(max_length=255, blank=True, null=True)
    gst_number = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return f"Seller Profile: {self.user.username}"