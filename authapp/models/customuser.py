from django.db import models
from django.contrib.auth.models import AbstractUser, Group, BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """Custom manager for CustomUser with email as USERNAME_FIELD"""
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    """Enhanced CustomUser with group-based user types and approval system"""
    
    ACCOUNT_STATUS_CHOICES = [
        ('unverified', 'Email Unverified'),
        ('verified', 'Email Verified'),
        ('pending_review', 'Pending Admin Review'),
        ('approved', 'Approved & Active'),
        ('rejected', 'Application Rejected'),
        ('suspended', 'Account Suspended'),
    ]
    
    username = None  # remove the username field
    email = models.EmailField(_("email address"), unique=True)

    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    
    # Verification and approval system
    is_email_verified = models.BooleanField(default=False)
    account_status = models.CharField(
        max_length=20,
        choices=ACCOUNT_STATUS_CHOICES,
        default='unverified'
    )
    
    # Approval tracking
    approved_by = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_users'
    )
    approved_at = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True, null=True)
    
    # Profile completion tracking
    # profile_completed = models.BooleanField(default=False)
    # documents_uploaded = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    @property
    def user_type(self):
        """Get user type based on group membership"""
        if self.groups.filter(name='Admin').exists():
            return 'admin'
        elif self.groups.filter(name='Developer').exists():
            return 'developer'
        elif self.groups.filter(name='Agent').exists():
            return 'agent'
        elif self.groups.filter(name='Seller').exists():
            return 'seller'
        elif self.groups.filter(name='Buyer').exists():
            return 'buyer'
        return 'buyer'  # default
    
    @property
    def is_approved(self):
        """Check if user account is approved and active"""
        return self.account_status == 'approved'
    
    @property
    def can_access_platform(self):
        """Check if user can access platform features"""
        # Buyers get access after email verification
        if self.user_type == 'buyer':
            return self.is_email_verified
        # Others need full approval
        return self.is_approved
    
    @property
    def requires_approval(self):
        """Check if user type requires admin approval"""
        return self.user_type in ['seller', 'agent', 'developer']
    
    def get_primary_group(self):
        """Get the primary group (user type) for this user"""
        groups = self.groups.all()
        if groups:
            return groups.first()
        return None
    
    def assign_to_group(self, group_name):
        """Assign user to a specific group"""
        try:
            group = Group.objects.get(name=group_name)
            self.groups.clear()  # Remove from all groups first
            self.groups.add(group)
            return True
        except Group.DoesNotExist:
            return False
    
    def has_group_permission(self, permission_codename):
        """Check if user has permission through their group"""
        return self.user_permissions.filter(codename=permission_codename).exists() or \
               self.groups.filter(permissions__codename=permission_codename).exists()