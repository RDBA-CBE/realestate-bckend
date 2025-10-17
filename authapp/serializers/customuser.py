from rest_framework import serializers
from authapp.models import CustomUser
from common.serializers import BaseSerializer


class CustomUserCreateSerializer(BaseSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"

class CustomUserListSerializer(BaseSerializer):
    user_type = serializers.ReadOnlyField()
    groups = serializers.StringRelatedField(many=True, read_only=True)
    primary_group = serializers.SerializerMethodField()
    
    class Meta:
        model = CustomUser
        exclude = ['password', 'last_login', 'is_superuser', 'is_staff', 'is_active', 'date_joined']
    
    def get_primary_group(self, obj):
        primary_group = obj.get_primary_group()
        return primary_group.name if primary_group else None

class CustomUserDetailSerializer(BaseSerializer):
    user_type = serializers.ReadOnlyField()
    groups = serializers.StringRelatedField(many=True, read_only=True)
    primary_group = serializers.SerializerMethodField()
    is_approved = serializers.ReadOnlyField()
    can_access_platform = serializers.ReadOnlyField()
    requires_approval = serializers.ReadOnlyField()
    
    class Meta:
        model = CustomUser
        fields = "__all__"
    
    def get_primary_group(self, obj):
        primary_group = obj.get_primary_group()
        return primary_group.name if primary_group else None

class CustomUserUpdateSerializer(BaseSerializer):
    class Meta:
        model = CustomUser
        exclude = ['last_login', 'is_superuser', 'is_staff', 'date_joined']