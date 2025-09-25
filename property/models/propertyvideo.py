from django.db import models
from common.models import BaseModel
from .property import Property


class PropertyVideo(BaseModel):
    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='videos'
    )
    video = models.FileField(upload_to='property_videos/%Y/%m/%d/')
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    thumbnail = models.ImageField(upload_to='property_video_thumbnails/%Y/%m/%d/', blank=True, null=True)
    duration = models.DurationField(blank=True, null=True, help_text="Video duration")
    file_size = models.PositiveIntegerField(blank=True, null=True, help_text="File size in bytes")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'Property Video'
        verbose_name_plural = 'Property Videos'
        ordering = ['order', 'created_at']
        unique_together = [['property', 'order']]

    def __str__(self):
        return f"Video: {self.title or 'Untitled'} for {self.property.title}"