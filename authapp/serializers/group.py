from rest_framework import serializers
from django.contrib.auth.models import Group, Permission


class PermissionSerializer(serializers.ModelSerializer):
    """Serializer for Permission model"""
    
    class Meta:
        model = Permission
        fields = ['id', 'name', 'codename', 'content_type']
        read_only_fields = ['id', 'codename', 'content_type']


class GroupListSerializer(serializers.ModelSerializer):
    """Serializer for listing groups"""
    user_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Group
        fields = ['id', 'name', 'user_count']
        read_only_fields = ['id']
    
    def get_user_count(self, obj):
        """Return the number of users in this group"""
        return obj.user_set.count()


class GroupDetailSerializer(serializers.ModelSerializer):
    """Serializer for detailed group view with permissions"""
    user_count = serializers.SerializerMethodField()
    users = serializers.SerializerMethodField()
    
    class Meta:
        model = Group
        fields = ['id', 'name', 'user_count', 'users']
        read_only_fields = ['id']
    
    def get_user_count(self, obj):
        """Return the number of users in this group"""
        return obj.user_set.count()
    
    def get_users(self, obj):
        """Return list of users in this group"""
        return [
            {
                'id': user.id,
                'email': user.email,
                'full_name': user.get_full_name() or user.email,
                'first_name': user.first_name,
                'last_name': user.last_name
            }
            for user in obj.user_set.all()[:10]  # Limit to first 10 users
        ]


class GroupCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating groups"""
    
    class Meta:
        model = Group
        fields = ['name']

    def create(self, validated_data):
        """Create a new group"""
        group = Group.objects.create(**validated_data)
        return group

    def validate_name(self, value):
        """Ensure group name is unique"""
        if Group.objects.filter(name__iexact=value).exists():
            raise serializers.ValidationError("A group with this name already exists")
        return value


class GroupUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating groups"""
    
    class Meta:
        model = Group
        fields = ['name']

    def validate_name(self, value):
        """Ensure group name is unique (excluding current instance)"""
        if Group.objects.filter(name__iexact=value).exclude(id=self.instance.id).exists():
            raise serializers.ValidationError("A group with this name already exists")
        return value


class AddUsersToGroupSerializer(serializers.Serializer):
    """Serializer for adding users to a group"""
    user_ids = serializers.ListField(
        child=serializers.IntegerField(),
        help_text="List of user IDs to add to the group"
    )
    
    def validate_user_ids(self, value):
        """Ensure all user IDs are valid"""
        from authapp.models import CustomUser
        valid_ids = set(CustomUser.objects.filter(id__in=value).values_list('id', flat=True))
        invalid_ids = set(value) - valid_ids
        if invalid_ids:
            raise serializers.ValidationError(f"Invalid user IDs: {', '.join(map(str, invalid_ids))}")
        return value


class RemoveUsersFromGroupSerializer(serializers.Serializer):
    """Serializer for removing users from a group"""
    user_ids = serializers.ListField(
        child=serializers.IntegerField(),
        help_text="List of user IDs to remove from the group"
    )
    
    def validate_user_ids(self, value):
        """Ensure all user IDs are valid"""
        from authapp.models import CustomUser
        valid_ids = set(CustomUser.objects.filter(id__in=value).values_list('id', flat=True))
        invalid_ids = set(value) - valid_ids
        if invalid_ids:
            raise serializers.ValidationError(f"Invalid user IDs: {', '.join(map(str, invalid_ids))}")
        return value
