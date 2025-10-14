from django.db import models
from property.models import Property  # assuming Property model exists


class FloorPlan(models.Model):
    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='floor_plans'
    )
    category = models.CharField(max_length=20)
    square_feet = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    image = models.ImageField(upload_to='floor_plans/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.property} - {self.category} ({self.square_feet} sqft)"
