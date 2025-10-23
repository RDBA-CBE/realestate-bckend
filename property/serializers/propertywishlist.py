from rest_framework import serializers
from common.serializers import BaseSerializer
from ..models import PropertyWishlist, Property
from .property import PropertyListSerializer



class PropertyWishlistListSerializer(BaseSerializer):
    """Serializer for listing user's wishlist"""
    property_count = serializers.SerializerMethodField()

    class Meta:
        model = PropertyWishlist
        fields = "__all__"

    def get_property_count(self, obj):
        return obj.property_count


class PropertyWishlistDetailSerializer(BaseSerializer):
    """Serializer for detailed wishlist view with properties"""
    properties = PropertyListSerializer(many=True, read_only=True)
    property_count = serializers.SerializerMethodField()

    class Meta:
        model = PropertyWishlist
        fields = "__all__"

    def get_property_count(self, obj):
        return obj.property_count


class PropertyWishlistCreateSerializer(BaseSerializer):
    """Serializer for creating wishlist - user can only have one wishlist"""

    class Meta:
        model = PropertyWishlist
        fields = ['name', 'description', 'is_public']
        
    def validate(self, attrs):
        """Ensure user doesn't already have a wishlist"""
        user = self.context['request'].user
        if PropertyWishlist.objects.filter(created_by=user).exists():
            raise serializers.ValidationError("You already have a wishlist. Each user can only have one wishlist.")
        return attrs


class PropertyWishlistUpdateSerializer(BaseSerializer):
    """Serializer for updating wishlist"""

    class Meta:
        model = PropertyWishlist
        fields = ['name', 'description', 'is_public']


class AddPropertyToWishlistSerializer(serializers.Serializer):
    """Serializer for adding properties to wishlist"""
    property_id = serializers.IntegerField(help_text="ID of the property to add")
    
    def validate_property_id(self, value):
        """Ensure property exists"""
        if not Property.objects.filter(id=value).exists():
            raise serializers.ValidationError(f"Property with ID {value} does not exist")
        return value


class RemovePropertyFromWishlistSerializer(serializers.Serializer):
    """Serializer for removing properties from wishlist"""
    property_id = serializers.IntegerField(help_text="ID of the property to remove")
    
    def validate_property_id(self, value):
        """Ensure property exists"""
        if not Property.objects.filter(id=value).exists():
            raise serializers.ValidationError(f"Property with ID {value} does not exist")
        return value