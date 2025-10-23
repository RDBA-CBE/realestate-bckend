from django.db import models
from common.models import BaseModel
from django.conf import settings
from .property import Property
from authapp.models import CustomUser


class PropertyFavorite(BaseModel):
    """Model for users to save favorite properties"""
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='favorites'
    )
    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='favorited_by'
    )
    notes = models.TextField(
        blank=True,
        help_text="Personal notes about this property"
    )

    class Meta:
        verbose_name = 'Property Favorite'
        verbose_name_plural = 'Property Favorites'
        unique_together = [['user', 'property']]
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email} favorited {self.property.title}"

class PropertyWishlist(BaseModel):
    name = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(blank=True)
    is_public = models.BooleanField(default=False)
    properties = models.ManyToManyField(Property, related_name='wishlists', blank=True)

    class Meta:
        verbose_name = 'Property Wishlist'
        verbose_name_plural = 'Property Wishlists'
        ordering = ['-created_at']
        # Ensure only one wishlist per user
        constraints = [
            models.UniqueConstraint(
                fields=['created_by'], 
                name='unique_wishlist_per_user'
            )
        ]

    def __str__(self):
        return f"{self.created_by.get_full_name() or self.created_by.email}'s wishlist"

    @property
    def property_count(self):
        """Return the number of properties in this wishlist."""
        return self.properties.count()

class PropertyAlert(BaseModel):
    """Model for users to set up alerts for properties matching their criteria"""
    ALERT_FREQUENCY_CHOICES = [
        ('instant', 'Instant'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    ]

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='property_alerts'
    )
    name = models.CharField(max_length=100)
    
    # Search Criteria
    cities = models.JSONField(
        default=list,
        help_text="List of cities to search in"
    )
    property_types = models.JSONField(
        default=list,
        help_text="List of property types"
    )
    listing_types = models.JSONField(
        default=list,
        help_text="List of listing types (sale, rent, lease)"
    )
    
    # Price Range
    min_price = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True
    )
    max_price = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True
    )
    
    # Property Requirements
    min_bedrooms = models.PositiveIntegerField(null=True, blank=True)
    min_bathrooms = models.PositiveIntegerField(null=True, blank=True)
    min_area = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    max_area = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    
    # Features
    required_features = models.JSONField(
        default=list,
        help_text="List of required feature IDs"
    )
    
    # Alert Settings
    is_active = models.BooleanField(default=True)
    frequency = models.CharField(
        max_length=10,
        choices=ALERT_FREQUENCY_CHOICES,
        default='daily'
    )
    last_sent = models.DateTimeField(null=True, blank=True)
    
    # Delivery Options
    email_alerts = models.BooleanField(default=True)
    sms_alerts = models.BooleanField(default=False)
    push_notifications = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Property Alert'
        verbose_name_plural = 'Property Alerts'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email}'s alert: {self.name}"

    def matches_property(self, property_obj):
        """Check if a property matches this alert's criteria"""
        # Check cities
        if self.cities and property_obj.city not in self.cities:
            return False
            
        # Check property types
        if self.property_types and property_obj.property_type not in self.property_types:
            return False
            
        # Check listing types
        if self.listing_types and property_obj.listing_type not in self.listing_types:
            return False
            
        # Check price range
        if self.min_price and property_obj.price < self.min_price:
            return False
        if self.max_price and property_obj.price > self.max_price:
            return False
            
        # Check bedrooms
        if self.min_bedrooms and property_obj.bedrooms < self.min_bedrooms:
            return False
            
        # Check bathrooms
        if self.min_bathrooms and property_obj.bathrooms < self.min_bathrooms:
            return False
            
        # Check area
        if self.min_area and property_obj.total_area < self.min_area:
            return False
        if self.max_area and property_obj.total_area > self.max_area:
            return False
            
        # Check required features
        if self.required_features:
            property_feature_ids = list(
                property_obj.property_features.values_list('feature_id', flat=True)
            )
            for required_feature_id in self.required_features:
                if required_feature_id not in property_feature_ids:
                    return False
                    
        return True

class PropertyComparison(BaseModel):
    """Model for users to compare multiple properties"""
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='property_comparisons'
    )
    name = models.CharField(max_length=100)
    properties = models.ManyToManyField(
        Property,
        related_name='comparisons'
    )
    notes = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Property Comparison'
        verbose_name_plural = 'Property Comparisons'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email}'s comparison: {self.name}"

    @property
    def property_count(self):
        return self.properties.count()


