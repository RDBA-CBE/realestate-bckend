from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from common.models import BaseModel
from .customuser import CustomUser


class Property(BaseModel):
    PROPERTY_TYPE_CHOICES = [
        ('apartment', 'Apartment'),
        ('house', 'House'),
        ('condo', 'Condo'),
        ('townhouse', 'Townhouse'),
        ('villa', 'Villa'),
        ('studio', 'Studio'),
        ('duplex', 'Duplex'),
        ('penthouse', 'Penthouse'),
        ('commercial', 'Commercial'),
        ('office', 'Office'),
        ('warehouse', 'Warehouse'),
        ('land', 'Land'),
        ('other', 'Other'),
    ]

    LISTING_TYPE_CHOICES = [
        ('sale', 'For Sale'),
        ('rent', 'For Rent'),
        ('lease', 'For Lease'),
    ]

    STATUS_CHOICES = [
        ('available', 'Available'),
        ('sold', 'Sold'),
        ('rented', 'Rented'),
        ('under_contract', 'Under Contract'),
        ('off_market', 'Off Market'),
        ('pending', 'Pending'),
    ]

    FURNISHING_CHOICES = [
        ('furnished', 'Furnished'),
        ('semi_furnished', 'Semi Furnished'),
        ('unfurnished', 'Unfurnished'),
    ]

    PARKING_CHOICES = [
        ('none', 'No Parking'),
        ('street', 'Street Parking'),
        ('garage', 'Garage'),
        ('covered', 'Covered Parking'),
        ('open', 'Open Parking'),
    ]

    # Basic Information
    title = models.CharField(max_length=255)
    description = models.TextField()
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPE_CHOICES)
    listing_type = models.CharField(max_length=10, choices=LISTING_TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')

    # Owner/Agent Information
    owner = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='owned_properties'
    )
    agent = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='managed_properties'
    )

    # Location Information
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default='India')
    postal_code = models.CharField(max_length=20)
    latitude = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)

    # Property Details
    bedrooms = models.PositiveIntegerField(default=0)
    bathrooms = models.PositiveIntegerField(default=0)
    total_area = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        help_text="Total area in square feet"
    )
    carpet_area = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True,
        help_text="Carpet area in square feet"
    )
    built_year = models.PositiveIntegerField(
        null=True, 
        blank=True,
        validators=[MinValueValidator(1800), MaxValueValidator(2030)]
    )
    floor_number = models.PositiveIntegerField(null=True, blank=True)
    total_floors = models.PositiveIntegerField(null=True, blank=True)

    # Pricing Information
    price = models.DecimalField(max_digits=15, decimal_places=2)
    price_per_sqft = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True
    )
    maintenance_charges = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True
    )
    security_deposit = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        null=True, 
        blank=True
    )

    # Property Features
    furnishing = models.CharField(
        max_length=20, 
        choices=FURNISHING_CHOICES, 
        default='unfurnished'
    )
    parking = models.CharField(
        max_length=20, 
        choices=PARKING_CHOICES, 
        default='none'
    )
    parking_spaces = models.PositiveIntegerField(default=0)
    
    # Amenities (Boolean fields for common amenities)
    has_balcony = models.BooleanField(default=False)
    has_garden = models.BooleanField(default=False)
    has_swimming_pool = models.BooleanField(default=False)
    has_gym = models.BooleanField(default=False)
    has_elevator = models.BooleanField(default=False)
    has_security = models.BooleanField(default=False)
    has_power_backup = models.BooleanField(default=False)
    has_air_conditioning = models.BooleanField(default=False)
    pet_friendly = models.BooleanField(default=False)

    # Availability
    available_from = models.DateField(null=True, blank=True)
    
    # SEO and Display
    slug = models.SlugField(max_length=300, unique=True, null=True, blank=True)
    is_featured = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    
    # Statistics
    views_count = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'Property'
        verbose_name_plural = 'Properties'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['city', 'property_type']),
            models.Index(fields=['listing_type', 'status']),
            models.Index(fields=['price']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.title} - {self.city}"

    def save(self, *args, **kwargs):
        # Auto-calculate price per square foot
        if self.price and self.total_area:
            self.price_per_sqft = self.price / self.total_area
        
        # Generate slug if not provided
        if not self.slug:
            from django.utils.text import slugify
            base_slug = slugify(f"{self.title}-{self.city}")
            slug = base_slug
            counter = 1
            while Property.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
            
        super().save(*args, **kwargs)

    @property
    def full_address(self):
        return f"{self.address}, {self.city}, {self.state} {self.postal_code}"

    @property
    def is_available(self):
        return self.status == 'available'

    @property
    def average_rating(self):
        reviews = self.reviews.all()
        if reviews:
            return sum(review.rating for review in reviews) / len(reviews)
        return 0

    @property
    def total_reviews(self):
        return self.reviews.count()