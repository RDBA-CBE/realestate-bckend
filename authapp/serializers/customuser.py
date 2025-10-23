from rest_framework import serializers
from authapp.models import CustomUser
from common.serializers import BaseSerializer


class CustomUserCreateSerializer(BaseSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"

    def create(self, validated_data):
        # Handle password and groups (many-to-many)
        password = validated_data.pop('password', None)
        groups = validated_data.pop('groups', None)
        # also support singular 'group' for backward compatibility
        if groups is None:
            groups = validated_data.pop('group', None)

        user = CustomUser(**validated_data)
        if password:
            user.set_password(password)
        user.save()

        # Set groups correctly using set(); accept list of ids or Group instances
        if groups is not None:
            from django.contrib.auth.models import Group
            # if groups is a single Group instance, wrap into list
            if not isinstance(groups, (list, tuple)):
                groups = [groups]

            # if provided as ints (ids), resolve to Group queryset
            if groups and all(isinstance(g, int) for g in groups):
                qs = Group.objects.filter(id__in=groups)
                user.groups.set(qs)
            else:
                # assume Group instances or other iterable acceptable to set()
                user.groups.set(groups)

        return user

class CustomUserListSerializer(BaseSerializer):
    user_type = serializers.ReadOnlyField()
    groups = serializers.StringRelatedField(many=True, read_only=True)
    primary_group = serializers.SerializerMethodField()
    profile_id = serializers.SerializerMethodField()
    wishlist_id = serializers.SerializerMethodField()
    
    class Meta:
        model = CustomUser
        exclude = ['password', 'last_login', 'is_superuser', 'is_staff', 'is_active', 'date_joined']
    
    def get_primary_group(self, obj):
        primary_group = obj.get_primary_group()
        return primary_group.name if primary_group else None
    
    def get_profile_id(self, obj):
        """Return the profile ID based on user type"""
        user_type = obj.user_type
        try:
            if user_type == 'buyer' and hasattr(obj, 'buyer_profile'):
                return obj.buyer_profile.id
            elif user_type == 'seller' and hasattr(obj, 'seller_profile'):
                return obj.seller_profile.id
            elif user_type == 'agent' and hasattr(obj, 'agent_profile'):
                return obj.agent_profile.id
            elif user_type == 'developer' and hasattr(obj, 'developer_profile'):
                return obj.developer_profile.id
            elif user_type == 'admin' and hasattr(obj, 'admin_profile'):
                return obj.admin_profile.id
        except Exception:
            pass
        return None
    
    def get_wishlist_id(self, obj):
        """Return the wishlist ID for the user, if it exists"""
        from property.models import PropertyWishlist
        try:
            wishlist = PropertyWishlist.objects.get(created_by=obj)
            return wishlist.id
        except PropertyWishlist.DoesNotExist:
            return None

class CustomUserDetailSerializer(BaseSerializer):
    user_type = serializers.ReadOnlyField()
    groups = serializers.StringRelatedField(many=True, read_only=True)
    primary_group = serializers.SerializerMethodField()
    is_approved = serializers.ReadOnlyField()
    can_access_platform = serializers.ReadOnlyField()
    requires_approval = serializers.ReadOnlyField()
    profile = serializers.SerializerMethodField()
    
    class Meta:
        model = CustomUser
        exclude = ['password', 'last_login', 'is_superuser', 'is_staff', 'is_active', 'date_joined']
    
    def get_primary_group(self, obj):
        primary_group = obj.get_primary_group()
        return primary_group.name if primary_group else None
    
    
    def get_profile(self, obj):
        """Dynamically return the appropriate profile based on user type"""
        user_type = obj.user_type
        
        try:
            if user_type == 'buyer' and hasattr(obj, 'buyer_profile'):
                from .buyerprofile import BuyerProfileDetailSerializer
                return BuyerProfileDetailSerializer(obj.buyer_profile).data
                
            elif user_type == 'seller' and hasattr(obj, 'seller_profile'):
                from .seller_profile import SellerProfileDetailSerializer
                return SellerProfileDetailSerializer(obj.seller_profile).data
                
            elif user_type == 'agent' and hasattr(obj, 'agent_profile'):
                from .agent_profile import AgentProfileDetailSerializer
                return AgentProfileDetailSerializer(obj.agent_profile).data
                
            elif user_type == 'developer' and hasattr(obj, 'developer_profile'):
                from .developer_profile import DeveloperProfileDetailSerializer
                return DeveloperProfileDetailSerializer(obj.developer_profile).data
                
            elif user_type == 'admin' and hasattr(obj, 'admin_profile'):
                from .admin_profile import AdminProfileDetailSerializer
                return AdminProfileDetailSerializer(obj.admin_profile).data
                
        except Exception as e:
            return None
        
        return None

class CustomUserUpdateSerializer(BaseSerializer):
    class Meta:
        model = CustomUser
        exclude = ['last_login', 'is_superuser', 'is_staff', 'date_joined']
    
    def update(self, instance, validated_data):
        # Handle password if provided
        password = validated_data.pop('password', None)
        groups = validated_data.pop('groups', None)

        # Apply other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()

        # Update groups if provided
        if groups is not None:
            from django.contrib.auth.models import Group
            if not isinstance(groups, (list, tuple)):
                groups = [groups]
            if groups and all(isinstance(g, int) for g in groups):
                qs = Group.objects.filter(id__in=groups)
                instance.groups.set(qs)
            else:
                instance.groups.set(groups)

        return instance