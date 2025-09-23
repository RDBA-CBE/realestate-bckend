
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from ..utils import UserGroupManager

User = get_user_model()



class RegistrationSerializer(serializers.ModelSerializer):
    """Enhanced registration serializer with user type support"""

    USER_TYPE_CHOICES = [
        ('buyer', 'Property Buyer'),
        ('seller', 'Property Seller'),
        ('agent', 'Real Estate Agent'),
        ('developer', 'Property Developer'),
    ]

    user_type = serializers.ChoiceField(
        choices=USER_TYPE_CHOICES,
        default='buyer',
        help_text="Select your role in the real estate platform"
    )
    password = serializers.CharField(write_only=True, min_length=8)
    terms_accepted = serializers.BooleanField(
        write_only=True,
        help_text="You must accept the terms and conditions"
    )
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=30)

    class Meta:
        model = User
        fields = [
            'email', 'first_name', 'last_name', 'phone',
            'user_type', 'password', 'terms_accepted'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'phone': {'required': False}
        }

    def validate_password(self, value):
        """Validate password strength"""
        try:
            validate_password(value)
        except DjangoValidationError as e:
            raise serializers.ValidationError(list(e.messages))
        return value

    def validate(self, attrs):
        """Validate registration data"""
        # Check if terms are accepted
        if not attrs.get('terms_accepted'):
            raise serializers.ValidationError({
                'terms_accepted': 'You must accept the terms and conditions.'
            })

        # Validate email uniqueness
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({
                'email': 'A user with this email already exists.'
            })

        return attrs

    def create(self, validated_data):
        """Create user with appropriate group assignment"""
        # Remove fields not needed for user creation
        user_type = validated_data.pop('user_type')
        validated_data.pop('terms_accepted')

        # Create user
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)

        # Store user type for signal handler
        user._user_type = user_type

        # Set initial account status based on user type
        if UserGroupManager.get_instant_access(user_type):
            user.account_status = 'verified'  # Will be set to approved after email verification
        else:
            user.account_status = 'unverified'

        user.save()

        return user

    def to_representation(self, instance):
        """Customize response data"""
        data = super().to_representation(instance)

        # Add user type and workflow information
        user_type = instance.user_type
        workflow = UserGroupManager.get_approval_workflow(user_type)

        data.update({
            'user_type': user_type,
            'account_status': instance.account_status,
            'requires_approval': UserGroupManager.requires_approval(user_type),
            'next_steps': workflow['steps'],
            'workflow_message': workflow.get('approval_message', '')
        })

        # Remove sensitive information
        data.pop('password', None)

        return data


class UserTypeChangeSerializer(serializers.Serializer):
    """Serializer for changing user type (admin only)"""
    
    USER_TYPE_CHOICES = [
        ('buyer', 'Property Buyer'),
        ('seller', 'Property Seller'),
        ('agent', 'Real Estate Agent'),
        ('developer', 'Property Developer'),
        ('admin', 'System Administrator'),
    ]
    
    user_id = serializers.IntegerField()
    new_user_type = serializers.ChoiceField(choices=USER_TYPE_CHOICES)
    reason = serializers.CharField(max_length=500, required=False)

    def validate_user_id(self, value):
        """Validate user exists"""
        try:
            user = User.objects.get(id=value)
            return value
        except User.DoesNotExist:
            raise serializers.ValidationError("User does not exist.")

    def validate(self, attrs):
        """Validate user type change request"""
        user = User.objects.get(id=attrs['user_id'])
        new_type = attrs['new_user_type']
        current_type = user.user_type
        
        # Prevent changing to same type
        if current_type == new_type:
            raise serializers.ValidationError({
                'new_user_type': f'User is already a {new_type}.'
            })
        
        # Additional validation rules can be added here
        return attrs


class AccountApprovalSerializer(serializers.Serializer):
    """Serializer for account approval/rejection"""
    
    STATUS_CHOICES = [
        ('approved', 'Approve Account'),
        ('rejected', 'Reject Account'),
        ('suspended', 'Suspend Account'),
    ]
    
    user_id = serializers.IntegerField()
    action = serializers.ChoiceField(choices=STATUS_CHOICES)
    notes = serializers.CharField(max_length=1000, required=False)
    rejection_reason = serializers.CharField(max_length=500, required=False)

    def validate_user_id(self, value):
        """Validate user exists"""
        try:
            user = User.objects.get(id=value)
            return value
        except User.DoesNotExist:
            raise serializers.ValidationError("User does not exist.")

    def validate(self, attrs):
        """Validate approval action"""
        user = User.objects.get(id=attrs['user_id'])
        action = attrs['action']
        
        # Check if rejection reason is provided for rejection
        if action == 'rejected' and not attrs.get('rejection_reason'):
            raise serializers.ValidationError({
                'rejection_reason': 'Rejection reason is required when rejecting an account.'
            })
        
        # Check if user is in appropriate status for action
        if user.account_status == 'approved' and action == 'approved':
            raise serializers.ValidationError({
                'action': 'User account is already approved.'
            })
        
        return attrs