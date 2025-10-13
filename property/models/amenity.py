from django.db import models
from common.models import BaseModel


class Amenity(BaseModel):
    AMENITY_CATEGORIES = [
        ('indoor', 'Indoor Amenity'),
        ('outdoor', 'Outdoor Amenity'),
        ('building', 'Building Amenity'),
        ('security', 'Security Feature'),
        ('utilities', 'Utilities'),
        ('recreational', 'Recreational'),
        ('parking', 'Parking Related'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=20, choices=AMENITY_CATEGORIES, default='other')
    icon = models.CharField(max_length=50, blank=True, help_text="Icon class name for UI display")
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Amenity'
        verbose_name_plural = 'Amenities'
        ordering = ['category', 'name']
    
    def __str__(self):
        return self.name