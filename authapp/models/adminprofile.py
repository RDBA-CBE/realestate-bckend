from django.db import models
from common.models import BaseModel
from models import CustomUser

class AdminProfile(BaseModel):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="admin_profile"
    )
    # Extra fields specific to Admins
    department = models.CharField(max_length=100, blank=True, null=True)
    designation = models.CharField(max_length=100, blank=True, null=True)
    office_phone = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"Admin Profile: {self.user.username}"
