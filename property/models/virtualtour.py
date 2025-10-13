from django.db import models
from common.models import BaseModel
from .property import Property


class VirtualTour(BaseModel):
    TOUR_TYPE_CHOICES = [
        ('360_view', '360 Degree View'),
        ('virtual_walkthrough', 'Virtual Walkthrough'),
        ('interactive_tour', 'Interactive Tour'),
        ('matterport', 'Matterport Tour'),
        ('google_tour', 'Google Street View Tour'),
        ('zillow_3d', 'Zillow 3D Tour'),
        ('other', 'Other'),
    ]

    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='virtual_tours'
    )
    tour_url = models.URLField(help_text="Third-party virtual tour link")
    tour_type = models.CharField(max_length=50, choices=TOUR_TYPE_CHOICES, default='360_view')
    description = models.TextField(blank=True)
    thumbnail = models.ImageField(upload_to='virtual_tour_thumbnails/%Y/%m/%d/', blank=True, null=True)
    provider = models.CharField(max_length=100, blank=True, help_text="e.g., Matterport, TourWrist, etc.")
    embed_code = models.TextField(blank=True, help_text="Embed HTML code if available")
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'Virtual Tour'
        verbose_name_plural = 'Virtual Tours'
        ordering = ['order', 'created_at']
        unique_together = [['property', 'order']]

    def __str__(self):
        return f"Virtual Tour: {self.title} for {self.property.title}"