from django.db import models
from common.models import BaseModel
from .property import Property


class PropertyImage(BaseModel):
    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(upload_to='property_images/%Y/%m/%d/')
    alt_text = models.CharField(max_length=255, blank=True)
    caption = models.CharField(max_length=500, blank=True)
    is_primary = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'Property Image'
        verbose_name_plural = 'Property Images'
        ordering = ['order', 'created_at']
        unique_together = [['property', 'order']]

    def __str__(self):
        return f"Image for {self.property.title}"

    def save(self, *args, **kwargs):
        # Ensure only one primary image per property
        if self.is_primary:
            PropertyImage.objects.filter(
                property=self.property,
                is_primary=True
            ).exclude(pk=self.pk).update(is_primary=False)
        
        # If this is the first image for the property, make it primary
        if not self.pk and not PropertyImage.objects.filter(property=self.property).exists():
            self.is_primary = True
            
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # If deleting primary image, make another image primary
        if self.is_primary:
            next_image = PropertyImage.objects.filter(
                property=self.property
            ).exclude(pk=self.pk).first()
            if next_image:
                next_image.is_primary = True
                next_image.save()
        
        super().delete(*args, **kwargs)