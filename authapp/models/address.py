from django.db import models
from common.models import BaseModel
from .customuser import CustomUser

class Address(BaseModel):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="addresses"
    )
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default="India")  # change as needed
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    is_primary = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Addresses"

    def __str__(self):
        return f"{self.street}, {self.city}, {self.state}"


