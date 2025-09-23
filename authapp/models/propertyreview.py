from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from common.models import BaseModel
from .property import Property
from .customuser import CustomUser


class PropertyReview(BaseModel):
    """Model for property reviews and ratings"""
    property_obj = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    reviewer = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='property_reviews'
    )
    
    # Rating (1-5 stars)
    overall_rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Overall rating from 1-5"
    )
    
    # Detailed Ratings
    location_rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        null=True,
        blank=True,
        help_text="Location rating from 1-5"
    )
    value_for_money_rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        null=True,
        blank=True,
        help_text="Value for money rating from 1-5"
    )
    amenities_rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        null=True,
        blank=True,
        help_text="Amenities rating from 1-5"
    )
    maintenance_rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        null=True,
        blank=True,
        help_text="Maintenance rating from 1-5"
    )
    neighborhood_rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        null=True,
        blank=True,
        help_text="Neighborhood rating from 1-5"
    )
    
    # Review Content
    title = models.CharField(max_length=200)
    review_text = models.TextField()
    
    # Review Details
    stayed_duration = models.CharField(
        max_length=50,
        blank=True,
        help_text="How long did you stay/live here?"
    )
    relationship_to_property = models.CharField(
        max_length=20,
        choices=[
            ('owner', 'Owner'),
            ('tenant', 'Tenant/Renter'),
            ('visitor', 'Visitor'),
            ('buyer', 'Potential Buyer'),
            ('neighbor', 'Neighbor'),
        ],
        default='visitor'
    )
    
    # Pros and Cons
    pros = models.TextField(blank=True, help_text="What did you like?")
    cons = models.TextField(blank=True, help_text="What could be improved?")
    
    # Recommendations
    would_recommend = models.BooleanField(null=True, blank=True)
    recommended_for = models.JSONField(
        default=list,
        help_text="List of user types this is recommended for (families, students, professionals, etc.)"
    )
    
    # Verification and Moderation
    is_verified = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    
    # Interaction
    helpful_count = models.PositiveIntegerField(default=0)
    not_helpful_count = models.PositiveIntegerField(default=0)
    
    # Response from Property Owner/Agent
    owner_response = models.TextField(blank=True)
    owner_response_date = models.DateTimeField(null=True, blank=True)
    responded_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='review_responses'
    )

    class Meta:
        verbose_name = 'Property Review'
        verbose_name_plural = 'Property Reviews'
        unique_together = [['property_obj', 'reviewer']]  # One review per user per property
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['property_obj', 'is_approved']),
            models.Index(fields=['overall_rating']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"Review by {self.reviewer.email} for {self.property_obj.title}"

    @property
    def average_detailed_rating(self):
        """Calculate average of all detailed ratings"""
        ratings = [
            self.location_rating,
            self.value_for_money_rating,
            self.amenities_rating,
            self.maintenance_rating,
            self.neighborhood_rating
        ]
        valid_ratings = [r for r in ratings if r is not None]
        if valid_ratings:
            return sum(valid_ratings) / len(valid_ratings)
        return None

    @property
    def helpful_percentage(self):
        """Calculate percentage of helpful votes"""
        total_votes = self.helpful_count + self.not_helpful_count
        if total_votes > 0:
            return (self.helpful_count / total_votes) * 100
        return 0


class ReviewHelpfulness(BaseModel):
    """Model to track if users found reviews helpful"""
    review = models.ForeignKey(
        PropertyReview,
        on_delete=models.CASCADE,
        related_name='helpfulness_votes'
    )
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='review_votes'
    )
    is_helpful = models.BooleanField()  # True for helpful, False for not helpful

    class Meta:
        verbose_name = 'Review Helpfulness'
        verbose_name_plural = 'Review Helpfulness Votes'
        unique_together = [['review', 'user']]

    def __str__(self):
        helpful_text = "helpful" if self.is_helpful else "not helpful"
        return f"{self.user.email} found review {helpful_text}"

    def save(self, *args, **kwargs):
        # Update the helpfulness count on the review
        is_new = self.pk is None
        old_helpful = None
        
        if not is_new:
            old_helpful = ReviewHelpfulness.objects.get(pk=self.pk).is_helpful
            
        super().save(*args, **kwargs)
        
        # Update counts
        if is_new:
            if self.is_helpful:
                self.review.helpful_count += 1
            else:
                self.review.not_helpful_count += 1
        else:
            # Vote changed
            if old_helpful != self.is_helpful:
                if self.is_helpful:
                    self.review.helpful_count += 1
                    self.review.not_helpful_count -= 1
                else:
                    self.review.helpful_count -= 1
                    self.review.not_helpful_count += 1
                    
        self.review.save(update_fields=['helpful_count', 'not_helpful_count'])

    def delete(self, *args, **kwargs):
        # Update counts when vote is deleted
        if self.is_helpful:
            self.review.helpful_count -= 1
        else:
            self.review.not_helpful_count -= 1
        self.review.save(update_fields=['helpful_count', 'not_helpful_count'])
        
        super().delete(*args, **kwargs)


class PropertyReport(BaseModel):
    """Model for reporting inappropriate content or issues with properties"""
    REPORT_TYPE_CHOICES = [
        ('fake_listing', 'Fake Listing'),
        ('wrong_info', 'Wrong Information'),
        ('spam', 'Spam'),
        ('inappropriate_content', 'Inappropriate Content'),
        ('duplicate', 'Duplicate Listing'),
        ('fraud', 'Fraudulent Activity'),
        ('other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('reviewing', 'Under Review'),
        ('resolved', 'Resolved'),
        ('dismissed', 'Dismissed'),
    ]

    property_obj = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='reports'
    )
    reporter = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='property_reports'
    )
    report_type = models.CharField(max_length=30, choices=REPORT_TYPE_CHOICES)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Admin response
    admin_notes = models.TextField(blank=True)
    reviewed_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_reports'
    )
    reviewed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Property Report'
        verbose_name_plural = 'Property Reports'
        unique_together = [['property_obj', 'reporter', 'report_type']]
        ordering = ['-created_at']

    def __str__(self):
        return f"Report: {self.report_type} for {self.property_obj.title}"