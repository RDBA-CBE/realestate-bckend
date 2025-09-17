# models.py
from django.db import models
from common.models import BaseModel
from authapp.models import CustomUser

class AgentProfile(BaseModel):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, 
        related_name="agent_profile"
        )
    license_number = models.CharField(max_length=50)
    experience_years = models.IntegerField(default=0)

    def __str__(self):
        return f"Agent Profile: {self.user.username}"