from django.db.models.signals import post_migrate, post_save
from django.contrib.auth.models import Group
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

from .models import CustomUser
from .utils import UserGroupManager


def setup_groups(sender, **kwargs):
    """Create default groups after migration"""
    groups = ['Buyers', 'Sellers', 'Agents', 'Developers', 'Admins']
    for group_name in groups:
        Group.objects.get_or_create(name=group_name)


@receiver(post_save, sender=CustomUser)
def create_user_profile_and_assign_group(sender, instance, created, **kwargs):
    """Create user profile and assign to group based on registration"""
    if created:
        # Get user type from request or default to buyer
        user_type = getattr(instance, '_user_type', 'buyer')
        
        # Assign user to appropriate group
        try:
            UserGroupManager.assign_user_to_group(instance, user_type)
        except Exception as e:
            # Default to buyers group if assignment fails
            UserGroupManager.assign_user_to_group(instance, 'buyer')
        
        # Create appropriate profile based on user type
        create_user_profile(instance, user_type)
        
        # Send welcome email
        send_welcome_email(instance, user_type)


def create_user_profile(user, user_type):
    """Create appropriate profile based on user type"""
    from .models import BuyerProfile, SellerProfile, AgentProfile, DeveloperProfile, AdminProfile
    
    try:
        if user_type == 'buyer':
            BuyerProfile.objects.get_or_create(user=user)
        elif user_type == 'seller':
            SellerProfile.objects.get_or_create(user=user)
        elif user_type == 'agent':
            AgentProfile.objects.get_or_create(user=user)
        elif user_type == 'developer':
            DeveloperProfile.objects.get_or_create(user=user)
        elif user_type == 'admin':
            AdminProfile.objects.get_or_create(user=user)
    except Exception as e:
        # Default to buyer profile if creation fails
        BuyerProfile.objects.get_or_create(user=user)


@receiver(post_save, sender=CustomUser)
def handle_account_status_change(sender, instance, created, **kwargs):
    """Handle account status changes and send notifications"""
    if not created:
        # Check if account status changed
        if hasattr(instance, '_original_status'):
            if instance._original_status != instance.account_status:
                send_status_change_notification(instance)


def send_welcome_email(user, user_type):
    """Send welcome email based on user type"""
    try:
        workflow = UserGroupManager.get_approval_workflow(user_type)
        
        subject = f'Welcome to Real Estate Platform - {user.get_full_name()}'
        
        context = {
            'user': user,
            'user_type': user_type,
            'workflow': workflow,
            'next_steps': workflow['steps'],
            'requires_approval': UserGroupManager.requires_approval(user_type)
        }
        
        # Choose template based on user type
        template = f'emails/welcome_{user_type}.html'
        try:
            message = render_to_string(template, context)
        except:
            # Fallback to generic template
            message = render_to_string('emails/welcome_generic.html', context)
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            html_message=message,
            fail_silently=True,
        )
    except Exception as e:
        # Log error but don't fail user creation
        print(f"Failed to send welcome email: {e}")


def send_status_change_notification(user):
    """Send notification when account status changes"""
    try:
        status_messages = {
            'verified': 'Your email has been verified successfully!',
            'pending_review': 'Your account is now under review by our team.',
            'approved': 'Congratulations! Your account has been approved.',
            'rejected': 'Your account application has been rejected.',
            'suspended': 'Your account has been suspended.',
        }
        
        if user.account_status in status_messages:
            subject = f'Account Status Update - {status_messages[user.account_status]}'
            
            context = {
                'user': user,
                'status': user.account_status,
                'message': status_messages[user.account_status],
                'rejection_reason': getattr(user, 'rejection_reason', None)
            }
            
            message = render_to_string('emails/status_change.html', context)
            
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                html_message=message,
                fail_silently=True,
            )
    except Exception as e:
        print(f"Failed to send status change notification: {e}")


# Signal to track original status for comparison
@receiver(post_save, sender=CustomUser)
def track_status_changes(sender, instance, **kwargs):
    """Track status changes for notifications"""
    if instance.pk:
        try:
            original = CustomUser.objects.get(pk=instance.pk)
            instance._original_status = original.account_status
        except CustomUser.DoesNotExist:
            instance._original_status = None


# Signal for profile completion tracking
@receiver(post_save, sender=CustomUser)
def update_profile_completion(sender, instance, **kwargs):
    """Update user's profile completion status"""
    try:
        # Get the appropriate profile
        profile = None
        user_type = instance.user_type
        
        if user_type == 'buyer' and hasattr(instance, 'buyer_profile'):
            profile = instance.buyer_profile
        elif user_type == 'seller' and hasattr(instance, 'seller_profile'):
            profile = instance.seller_profile
        elif user_type == 'agent' and hasattr(instance, 'agent_profile'):
            profile = instance.agent_profile
        elif user_type == 'developer' and hasattr(instance, 'developer_profile'):
            profile = instance.developer_profile
        
        if profile:
            # Update profile completion status
            instance.profile_completed = profile.is_profile_complete()
            instance.documents_uploaded = getattr(profile, 'documents_uploaded', False)
            
            # Update account status based on completion and requirements
            if UserGroupManager.requires_approval(user_type):
                if profile.is_profile_complete() and not instance.is_approved:
                    instance.account_status = 'pending_review'
            else:
                if instance.is_email_verified and profile.is_profile_complete():
                    instance.account_status = 'approved'
            
            # Save without triggering signals again
            CustomUser.objects.filter(pk=instance.pk).update(
                profile_completed=instance.profile_completed,
                documents_uploaded=instance.documents_uploaded,
                account_status=instance.account_status
            )
    except Exception as e:
        print(f"Failed to update profile completion: {e}")
