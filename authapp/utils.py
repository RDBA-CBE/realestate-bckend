"""
Utility functions for group-based user type management
"""
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from .models import CustomUser


class UserGroupManager:
    """Utility class for managing user groups and permissions"""
    
    # Define user type hierarchy (higher index = higher privileges)
    USER_TYPE_HIERARCHY = ['buyer', 'seller', 'agent', 'developer', 'admin']
    
    # Define which user types require approval
    APPROVAL_REQUIRED_TYPES = ['seller', 'agent', 'developer']
    
    # Define instant access user types (no approval needed)
    INSTANT_ACCESS_TYPES = ['buyer']
    
    @staticmethod
    def get_group_name(user_type):
        """Convert user type to group name"""
        group_mapping = {
            'buyer': 'Buyers',
            'seller': 'Sellers',
            'agent': 'Agents',
            'developer': 'Developers',
            'admin': 'Admins'
        }
        return group_mapping.get(user_type)
    
    @staticmethod
    def assign_user_to_group(user, user_type):
        """Assign user to appropriate group based on user type"""
        group_name = UserGroupManager.get_group_name(user_type)
        if not group_name:
            raise ValidationError(f"Invalid user type: {user_type}")
        
        try:
            group = Group.objects.get(name=group_name)
            # Clear existing groups and assign new one
            user.groups.clear()
            user.groups.add(group)
            return True
        except Group.DoesNotExist:
            raise ValidationError(f"Group {group_name} does not exist. Run setup_user_groups command.")
    
    @staticmethod
    def get_user_type(user):
        """Get user type based on group membership"""
        return user.user_type
    
    @staticmethod
    def requires_approval(user_type):
        """Check if user type requires admin approval"""
        return user_type in UserGroupManager.APPROVAL_REQUIRED_TYPES
    
    @staticmethod
    def get_instant_access(user_type):
        """Check if user type gets instant access after email verification"""
        return user_type in UserGroupManager.INSTANT_ACCESS_TYPES
    
    @staticmethod
    def can_access_feature(user, feature_permission):
        """Check if user can access a specific feature"""
        if not user.is_authenticated:
            return False
        
        # Check if user account is in good standing
        if not user.can_access_platform:
            return False
        
        # Check permission through groups
        return user.has_group_permission(feature_permission)
    
    @staticmethod
    def get_user_permissions(user):
        """Get list of all permissions for a user"""
        if not user.is_authenticated:
            return []
        
        # Get permissions from groups
        group_permissions = Permission.objects.filter(group__user=user)
        
        # Get direct user permissions
        user_permissions = user.user_permissions.all()
        
        # Combine and deduplicate
        all_permissions = group_permissions.union(user_permissions)
        
        return list(all_permissions.values_list('codename', flat=True))
    
    @staticmethod
    def user_has_higher_privilege(user1, user2):
        """Check if user1 has higher privilege than user2"""
        type1 = user1.user_type
        type2 = user2.user_type
        
        try:
            index1 = UserGroupManager.USER_TYPE_HIERARCHY.index(type1)
            index2 = UserGroupManager.USER_TYPE_HIERARCHY.index(type2)
            return index1 > index2
        except ValueError:
            return False
    
    @staticmethod
    def get_approval_workflow(user_type):
        """Get the approval workflow for a user type"""
        workflows = {
            'buyer': {
                'steps': ['email_verification'],
                'auto_approve': True,
                'requires_documents': False,
                'approval_message': 'Account ready to use!'
            },
            'seller': {
                'steps': ['email_verification', 'document_upload', 'admin_review'],
                'auto_approve': False,
                'requires_documents': True,
                'approval_message': 'Account approved! You can now list properties.'
            },
            'agent': {
                'steps': ['email_verification', 'license_upload', 'agency_verification', 'admin_review'],
                'auto_approve': False,
                'requires_documents': True,
                'approval_message': 'Agent account approved! You can now manage client properties.'
            },
            'developer': {
                'steps': ['email_verification', 'company_verification', 'portfolio_review', 'admin_review'],
                'auto_approve': False,
                'requires_documents': True,
                'approval_message': 'Developer account approved! You can now create projects.'
            },
            'admin': {
                'steps': ['invitation_only'],
                'auto_approve': False,
                'requires_documents': False,
                'approval_message': 'Admin account activated.'
            }
        }
        return workflows.get(user_type, workflows['buyer'])


class PermissionChecker:
    """Utility class for checking specific permissions"""
    
    @staticmethod
    def can_list_property(user):
        """Check if user can list properties"""
        return UserGroupManager.can_access_feature(user, 'add_property')
    
    @staticmethod
    def can_view_property(user, property_obj=None):
        """Check if user can view properties"""
        return UserGroupManager.can_access_feature(user, 'view_property')
    
    @staticmethod
    def can_edit_property(user, property_obj):
        """Check if user can edit a specific property"""
        if not UserGroupManager.can_access_feature(user, 'change_property'):
            return False
        
        # Additional business logic checks
        user_type = user.user_type
        
        if user_type == 'admin':
            return True
        elif user_type == 'seller':
            return property_obj.owner == user
        elif user_type == 'agent':
            return property_obj.agent == user or property_obj.owner == user
        elif user_type == 'developer':
            return property_obj.owner == user
        
        return False
    
    @staticmethod
    def can_delete_property(user, property_obj):
        """Check if user can delete a specific property"""
        if not UserGroupManager.can_access_feature(user, 'delete_property'):
            return False
        
        # Only owner, assigned agent, or admin can delete
        user_type = user.user_type
        
        if user_type == 'admin':
            return True
        elif user_type in ['seller', 'developer']:
            return property_obj.owner == user
        elif user_type == 'agent':
            return property_obj.agent == user
        
        return False
    
    @staticmethod
    def can_manage_inquiry(user, inquiry_obj):
        """Check if user can manage a property inquiry"""
        user_type = user.user_type
        
        if user_type == 'admin':
            return True
        elif user_type == 'buyer':
            return inquiry_obj.inquirer == user
        elif user_type in ['seller', 'developer']:
            return inquiry_obj.property.owner == user
        elif user_type == 'agent':
            return inquiry_obj.property.agent == user or inquiry_obj.assigned_to == user
        
        return False
    
    @staticmethod
    def can_approve_user(approver, user_to_approve):
        """Check if approver can approve another user's account"""
        if approver.user_type != 'admin':
            return False
        
        # Admins can approve all user types except other admins
        return user_to_approve.user_type != 'admin'


# Decorator for group-based permission checking
def group_required(allowed_groups):
    """Decorator to check if user belongs to allowed groups"""
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                from django.http import JsonResponse
                return JsonResponse({'error': 'Authentication required'}, status=401)
            
            user_group = request.user.get_primary_group()
            if not user_group or user_group.name not in allowed_groups:
                from django.http import JsonResponse
                return JsonResponse({'error': 'Insufficient permissions'}, status=403)
            
            if not request.user.can_access_platform:
                from django.http import JsonResponse
                return JsonResponse({'error': 'Account not approved'}, status=403)
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


# Decorator for user type checking
def user_type_required(allowed_types):
    """Decorator to check if user has required user type"""
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                from django.http import JsonResponse
                return JsonResponse({'error': 'Authentication required'}, status=401)
            
            if request.user.user_type not in allowed_types:
                from django.http import JsonResponse
                return JsonResponse({'error': 'Insufficient permissions'}, status=403)
            
            if not request.user.can_access_platform:
                from django.http import JsonResponse
                return JsonResponse({'error': 'Account not approved'}, status=403)
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator