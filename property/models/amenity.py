from django.db import models
from common.models import BaseModel


class Amenity(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return f"Amenity {self.id}: {self.name}"