from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings

from authapp.serializers.register import (
    RegistrationSerializer, 
    UserTypeChangeSerializer,
    AccountApprovalSerializer
)
from authapp.utils import UserGroupManager, user_type_required

User = get_user_model()


class RegistrationViewSet(viewsets.ModelViewSet):
    """Enhanced User Registration ViewSet with group-based user types"""
    
    serializer_class = RegistrationSerializer
    queryset = User.objects.all()
    http_method_names = ['post']
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        request=RegistrationSerializer,
        responses={
            201: {
                "type": "object",
                "properties": {
                    "success": {"type": "string"},
                    "user": {"type": "object"},
                    "message": {"type": "string"}
                }
            }
        },
        summary="Register a new user with user type selection",
        description="Register a new user and automatically assign them to the appropriate group based on their selected user type."
    )
    def create(self, request, *args, **kwargs):
        """Create a new user with automatic group assignment"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.save()
        user_type = user.user_type
        
        # Get workflow information
        workflow = UserGroupManager.get_approval_workflow(user_type)
        
        # Prepare response message
        if UserGroupManager.requires_approval(user_type):
            message = f"Registration successful! Please complete your {user_type} profile and upload required documents for approval."
        else:
            message = "Registration successful! Please verify your email to start using the platform."
        
        response_data = {
            "success": "User created successfully",
            "user": {
                "id": user.id,
                "email": user.email,
                "user_type": user_type,
                "account_status": user.account_status,
                "requires_approval": UserGroupManager.requires_approval(user_type)
            },
            "message": message,
            "next_steps": workflow['steps']
        }
        
        return Response(response_data, status=status.HTTP_201_CREATED)


class UserManagementViewSet(viewsets.GenericViewSet):
    """ViewSet for user management operations (admin only)"""
    
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'change_user_type':
            return UserTypeChangeSerializer
        elif self.action in ['approve_account', 'reject_account']:
            return AccountApprovalSerializer
        return RegistrationSerializer

    @extend_schema(
        request=UserTypeChangeSerializer,
        responses={200: {"success": "User type changed successfully"}},
        summary="Change user type (Admin only)",
    )
    @action(detail=False, methods=['post'])
    @user_type_required(['admin'])
    def change_user_type(self, request):
        """Change a user's type and reassign groups"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user_id = serializer.validated_data['user_id']
        new_user_type = serializer.validated_data['new_user_type']
        reason = serializer.validated_data.get('reason', '')
        
        user = User.objects.get(id=user_id)
        old_user_type = user.user_type
        
        # Reassign to new group
        UserGroupManager.assign_user_to_group(user, new_user_type)
        
        # Reset account status if changing to a type that requires approval
        if UserGroupManager.requires_approval(new_user_type):
            user.account_status = 'pending_review'
        
        user.save()
        
        # Log the change (you might want to add an audit log model)
        # AuditLog.objects.create(
        #     action='user_type_change',
        #     performed_by=request.user,
        #     target_user=user,
        #     details=f'Changed from {old_user_type} to {new_user_type}. Reason: {reason}'
        # )
        
        return Response({
            "success": "User type changed successfully",
            "user": {
                "id": user.id,
                "email": user.email,
                "old_user_type": old_user_type,
                "new_user_type": new_user_type,
                "account_status": user.account_status
            }
        })

    @extend_schema(
        request=AccountApprovalSerializer,
        responses={200: {"success": "Account approved successfully"}},
        summary="Approve user account (Admin only)",
    )
    @action(detail=False, methods=['post'])
    @user_type_required(['admin'])
    def approve_account(self, request):
        """Approve a user account"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user_id = serializer.validated_data['user_id']
        action = serializer.validated_data['action']
        notes = serializer.validated_data.get('notes', '')
        rejection_reason = serializer.validated_data.get('rejection_reason', '')
        
        user = User.objects.get(id=user_id)
        
        # Update user status
        user.account_status = action
        
        if action == 'approved':
            user.approved_by = request.user
            user.approved_at = timezone.now()
            user.rejection_reason = None
        elif action == 'rejected':
            user.rejection_reason = rejection_reason
            user.approved_by = None
            user.approved_at = None
        
        user.save()
        
        # Send notification email
        self.send_approval_notification(user, action, notes, rejection_reason)
        
        return Response({
            "success": f"Account {action} successfully",
            "user": {
                "id": user.id,
                "email": user.email,
                "user_type": user.user_type,
                "account_status": user.account_status,
                "approved_at": user.approved_at
            }
        })

    @extend_schema(
        responses={200: {"type": "array", "items": {"type": "object"}}},
        summary="Get pending approvals (Admin only)",
    )
    @action(detail=False, methods=['get'])
    @user_type_required(['admin'])
    def pending_approvals(self, request):
        """Get list of users pending approval"""
        pending_users = User.objects.filter(
            account_status='pending_review'
        ).select_related('buyer_profile', 'seller_profile', 'agent_profile', 'developer_profile')
        
        users_data = []
        for user in pending_users:
            # Get profile completion info
            profile = None
            user_type = user.user_type
            
            if user_type == 'seller' and hasattr(user, 'seller_profile'):
                profile = user.seller_profile
            elif user_type == 'agent' and hasattr(user, 'agent_profile'):
                profile = user.agent_profile
            elif user_type == 'developer' and hasattr(user, 'developer_profile'):
                profile = user.developer_profile
            
            users_data.append({
                "id": user.id,
                "email": user.email,
                "name": user.get_full_name(),
                "user_type": user_type,
                "account_status": user.account_status,
                "created_at": user.created_at,
                "profile_completed": user.profile_completed,
                "documents_uploaded": user.documents_uploaded,
                "profile_completion_percentage": getattr(profile, 'profile_completion_percentage', 0)
            })
        
        return Response(users_data)

    def send_approval_notification(self, user, action, notes, rejection_reason):
        """Send email notification for approval/rejection"""
        try:
            if action == 'approved':
                subject = 'Account Approved - Welcome to Real Estate Platform!'
                template = 'emails/account_approved.html'
            elif action == 'rejected':
                subject = 'Account Application Update'
                template = 'emails/account_rejected.html'
            else:
                return
            
            context = {
                'user': user,
                'action': action,
                'notes': notes,
                'rejection_reason': rejection_reason,
                'user_type': user.user_type
            }
            
            from django.template.loader import render_to_string
            message = render_to_string(template, context)
            
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                html_message=message,
                fail_silently=True,
            )
        except Exception as e:
            print(f"Failed to send approval notification: {e}")


class DashboardViewSet(viewsets.GenericViewSet):
    """ViewSet for user-type specific dashboard data"""
    
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        responses={200: {"type": "object"}},
        summary="Get user dashboard data",
    )
    @action(detail=False, methods=['get'])
    def dashboard_data(self, request):
        """Get dashboard data based on user type"""
        user = request.user
        
        if not user.can_access_platform:
            return Response({
                "error": "Account not approved or verified",
                "account_status": user.account_status,
                "user_type": user.user_type,
                "next_steps": UserGroupManager.get_approval_workflow(user.user_type)['steps']
            }, status=status.HTTP_403_FORBIDDEN)
        
        # Get user-type specific dashboard data
        dashboard_data = self.get_user_dashboard_data(user)
        
        return Response(dashboard_data)

    def get_user_dashboard_data(self, user):
        """Get dashboard data based on user type"""
        base_data = {
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.get_full_name(),
                "user_type": user.user_type,
                "account_status": user.account_status,
                "profile_completed": user.profile_completed
            }
        }
        
        user_type = user.user_type
        
        if user_type == 'buyer':
            return self.get_buyer_dashboard_data(user, base_data)
        elif user_type == 'seller':
            return self.get_seller_dashboard_data(user, base_data)
        elif user_type == 'agent':
            return self.get_agent_dashboard_data(user, base_data)
        elif user_type == 'developer':
            return self.get_developer_dashboard_data(user, base_data)
        elif user_type == 'admin':
            return self.get_admin_dashboard_data(user, base_data)
        
        return base_data

    def get_buyer_dashboard_data(self, user, base_data):
        """Get buyer-specific dashboard data"""
        # Add buyer-specific metrics
        base_data.update({
            "favorites_count": user.favorites.count() if hasattr(user, 'favorites') else 0,
            "inquiries_count": user.inquiries_made.count() if hasattr(user, 'inquiries_made') else 0,
            "recent_searches": [],  # Implement search history
            "recommended_properties": []  # Implement recommendation engine
        })
        return base_data

    def get_seller_dashboard_data(self, user, base_data):
        """Get seller-specific dashboard data"""
        base_data.update({
            "properties_count": user.owned_properties.count() if hasattr(user, 'owned_properties') else 0,
            "total_inquiries": 0,  # Sum of inquiries for all properties
            "recent_inquiries": [],
            "performance_metrics": {}
        })
        return base_data

    def get_agent_dashboard_data(self, user, base_data):
        """Get agent-specific dashboard data"""
        base_data.update({
            "managed_properties": user.managed_properties.count() if hasattr(user, 'managed_properties') else 0,
            "active_clients": 0,
            "recent_activities": [],
            "performance_metrics": {}
        })
        return base_data

    def get_developer_dashboard_data(self, user, base_data):
        """Get developer-specific dashboard data"""
        base_data.update({
            "total_projects": user.owned_properties.count() if hasattr(user, 'owned_properties') else 0,
            "total_units": 0,
            "sales_metrics": {},
            "project_status": {}
        })
        return base_data

    def get_admin_dashboard_data(self, user, base_data):
        """Get admin-specific dashboard data"""
        base_data.update({
            "total_users": User.objects.count(),
            "pending_approvals": User.objects.filter(account_status='pending_review').count(),
            "total_properties": 0,  # Get from Property model when available
            "system_metrics": {}
        })
        return base_data