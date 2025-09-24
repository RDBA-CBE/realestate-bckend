from django.db import models
from common.models import BaseModel
from .property import Property


class PropertyFeature(BaseModel):
    FEATURE_CATEGORY_CHOICES = [
        ('amenities', 'Amenities'),
        ('safety', 'Safety & Security'),
        ('connectivity', 'Connectivity'),
        ('recreation', 'Recreation'),
        ('utilities', 'Utilities'),
        ('convenience', 'Convenience'),
        ('environment', 'Environment'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=20, choices=FEATURE_CATEGORY_CHOICES)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="Icon class or name")
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Property Feature'
        verbose_name_plural = 'Property Features'
        ordering = ['category', 'name']

    def __str__(self):
        return self.name


class PropertyFeatureMapping(BaseModel):
    """Many-to-many relationship between Property and PropertyFeature with additional details"""
    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='property_features'
    )
    feature = models.ForeignKey(
        PropertyFeature,
        on_delete=models.CASCADE,
        related_name='property_mappings'
    )
    value = models.CharField(
        max_length=255, 
        blank=True,
        help_text="Additional value for the feature (e.g., '2 units' for AC)"
    )
    is_available = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Property Feature Mapping'
        verbose_name_plural = 'Property Feature Mappings'
        unique_together = [['property', 'feature']]

    def __str__(self):
        return f"{self.property.title} - {self.feature.name}"


# You can create initial features with a data migration or in Django admin
class NeighborhoodInfo(BaseModel):
    """Information about the neighborhood where the property is located"""
    property = models.OneToOneField(
        Property,
        on_delete=models.CASCADE,
        related_name='neighborhood'
    )
    
    # Transportation
    nearest_metro_station = models.CharField(max_length=200, blank=True)
    metro_distance = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        null=True, 
        blank=True,
        help_text="Distance in kilometers"
    )
    nearest_bus_stop = models.CharField(max_length=200, blank=True)
    bus_stop_distance = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        null=True, 
        blank=True,
        help_text="Distance in kilometers"
    )
    
    # Education
    nearest_school = models.CharField(max_length=200, blank=True)
    school_distance = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        null=True, 
        blank=True,
        help_text="Distance in kilometers"
    )
    nearest_college = models.CharField(max_length=200, blank=True)
    college_distance = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        null=True, 
        blank=True,
        help_text="Distance in kilometers"
    )
    
    # Healthcare
    nearest_hospital = models.CharField(max_length=200, blank=True)
    hospital_distance = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        null=True, 
        blank=True,
        help_text="Distance in kilometers"
    )
    
    # Shopping
    nearest_mall = models.CharField(max_length=200, blank=True)
    mall_distance = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        null=True, 
        blank=True,
        help_text="Distance in kilometers"
    )
    nearest_market = models.CharField(max_length=200, blank=True)
    market_distance = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        null=True, 
        blank=True,
        help_text="Distance in kilometers"
    )
    
    # Other amenities
    restaurants_nearby = models.PositiveIntegerField(default=0)
    atms_nearby = models.PositiveIntegerField(default=0)
    parks_nearby = models.PositiveIntegerField(default=0)
    
    # Ratings
    connectivity_rating = models.PositiveIntegerField(
        default=0,
        choices=[(i, i) for i in range(1, 6)],
        help_text="Rate connectivity from 1-5"
    )
    safety_rating = models.PositiveIntegerField(
        default=0,
        choices=[(i, i) for i in range(1, 6)],
        help_text="Rate safety from 1-5"
    )
    lifestyle_rating = models.PositiveIntegerField(
        default=0,
        choices=[(i, i) for i in range(1, 6)],
        help_text="Rate lifestyle from 1-5"
    )

    class Meta:
        verbose_name = 'Neighborhood Information'
        verbose_name_plural = 'Neighborhood Information'

    def __str__(self):
        return f"Neighborhood info for {self.property.title}"