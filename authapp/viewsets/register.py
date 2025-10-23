from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import Group
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
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        # Set account approval fields
        user.account_status = 'pending_review'
        user.is_active = False  # Disable login until admin approves
        user.save()

        user_type = serializer.validated_data.get("user_type")

        # 🔹 Assign Group based on user_type
        if user_type:
            group_name = user_type.capitalize()  # e.g., "buyer" → "Buyer"
            group, created = Group.objects.get_or_create(name=group_name)
            user.groups.add(group)

        # 🔹 Prepare response
        message = (
            "Registration successful! "
            "Your account has been submitted for admin review. "
            "You’ll receive an email notification once approved."
        )

        response_data = {
            "success": "User created successfully",
            "user": {
                "id": user.id,
                "email": user.email,
                "user_type": user_type,
                "account_status": user.account_status,
                "assigned_group": group_name if user_type else None,
                "requires_admin_approval": True,
            },
            "message": message,
            "next_steps": [
                "Wait for admin review and approval",
                "Check your email for approval notification",
                "Complete your profile after approval (if required)"
            ],
        }

        return Response(response_data, status=status.HTTP_201_CREATED)

    @extend_schema(
        request={
            "type": "object",
            "properties": {
                "email": {"type": "string", "format": "email"}
            }
        },
        responses={200: {"type": "object"}},
        summary="Check registration status by email",
    )
    @action(detail=False, methods=['post'])
    def check_status(self, request):
        """Check registration status by email (public endpoint)"""
        email = request.data.get('email')
        
        if not email:
            return Response({
                "error": "Email is required"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(email=email)
            
            status_messages = {
                'unverified': 'Account created but email not verified',
                'verified': 'Email verified, awaiting admin approval',
                'pending_review': 'Account under admin review',
                'approved': 'Account approved - you can now login',
                'rejected': 'Account application rejected',
                'suspended': 'Account suspended'
            }
            
            return Response({
                "email": user.email,
                "account_status": user.account_status,
                "status_message": status_messages.get(user.account_status, 'Unknown status'),
                "can_login": user.is_active and user.account_status == 'approved',
                "user_type": user.user_type,
                "created_at": user.created_at,
                "approved_at": user.approved_at,
                "rejection_reason": user.rejection_reason if user.account_status == 'rejected' else None
            })
            
        except User.DoesNotExist:
            return Response({
                "error": "No account found with this email address"
            }, status=status.HTTP_404_NOT_FOUND)

    def notify_admins_new_registration(self, user):
        """Notify admin users about new registration"""
        try:
            # Get all admin users
            admin_users = User.objects.filter(groups__name='Admin', is_active=True)
            admin_emails = [admin.email for admin in admin_users if admin.email]
            
            if admin_emails:
                subject = f'New User Registration - {user.user_type.title()}'
                message = f"""
                A new user has registered and is awaiting approval:
                
                Name: {user.get_full_name()}
                Email: {user.email}
                User Type: {user.user_type.title()}
                Registration Date: {user.created_at.strftime('%Y-%m-%d %H:%M')}
                
                Please review and approve/reject this registration in the admin panel.
                """
                
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    admin_emails,
                    fail_silently=True,
                )
        except Exception as e:
            print(f"Failed to send admin notification: {e}")

class DashboardViewSet(viewsets.GenericViewSet):
    """ViewSet for user-type specific dashboard data"""
    
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        responses={200: {"type": "object"}},
        summary="Check user account status",
    )
    @action(detail=False, methods=['get'])
    def account_status(self, request):
        """Check current user's account status"""
        user = request.user
        
        return Response({
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.get_full_name(),
                "user_type": user.user_type,
                "account_status": user.account_status,
                "is_active": user.is_active,
                "can_access_platform": user.account_status == 'approved' and user.is_active,
                "profile_completed": user.profile_completed,
                "approved_at": user.approved_at,
                "created_at": user.created_at
            },
            "status_info": {
                "pending_review": user.account_status == 'pending_review',
                "approved": user.account_status == 'approved',
                "rejected": user.account_status == 'rejected',
                "rejection_reason": user.rejection_reason if user.account_status == 'rejected' else None
            }
        })

    @extend_schema(
        responses={200: {"type": "object"}},
        summary="Get user dashboard data",
    )
    @action(detail=False, methods=['get'])
    def dashboard_data(self, request):
        """Get dashboard data based on user type"""
        user = request.user
        
        # Check if user can access the platform
        if user.account_status == 'pending_review':
            return Response({
                "message": "Your account is under review",
                "account_status": user.account_status,
                "user_type": user.user_type,
                "next_steps": [
                    "Wait for admin approval",
                    "Check your email for updates",
                    "Contact support if you have questions"
                ]
            }, status=status.HTTP_403_FORBIDDEN)
        
        if user.account_status == 'rejected':
            return Response({
                "error": "Your account application was rejected",
                "account_status": user.account_status,
                "rejection_reason": user.rejection_reason,
                "next_steps": [
                    "Contact support for more information",
                    "Address the issues mentioned in rejection reason",
                    "Reapply if permitted"
                ]
            }, status=status.HTTP_403_FORBIDDEN)
        
        if not user.is_active or user.account_status != 'approved':
            return Response({
                "error": "Account not yet approved for platform access",
                "account_status": user.account_status,
                "user_type": user.user_type,
                "next_steps": [
                    "Wait for admin approval",
                    "Verify your email if not done",
                    "Complete your profile if required"
                ]
            }, status=status.HTTP_403_FORBIDDEN)
        
        # Get user-type specific dashboard data for approved users
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