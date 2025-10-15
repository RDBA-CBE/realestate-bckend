from rest_framework import serializers
from common.serializers import BaseSerializer
from ..models import PropertyWishlist, PropertyWishlistItem
from .property import PropertyListSerializer



class PropertyWishlistListSerializer(BaseSerializer):
    """Serializer for listing user's wishlists"""
    property_count = serializers.SerializerMethodField()

    class Meta:
        model = PropertyWishlist
        fields = ['id', 'name', 'description', 'is_public', 'property_count', 'created_at']

    def get_property_count(self, obj):
        return obj.property_count


class PropertyWishlistDetailSerializer(BaseSerializer):
    """Serializer for detailed wishlist view with properties"""
    properties = PropertyListSerializer(many=True, read_only=True)
    property_count = serializers.SerializerMethodField()

    class Meta:
        model = PropertyWishlist
        fields = ['id', 'user', 'name', 'description', 'is_public', 'properties',
                 'property_count', 'created_at', 'updated_at']

    def get_property_count(self, obj):
        return obj.property_count


class PropertyWishlistCreateSerializer(BaseSerializer):
    """Serializer for creating wishlists"""

    class Meta:
        model = PropertyWishlist
        fields = ['name', 'description', 'is_public']

    def validate_name(self, value):
        """Ensure user doesn't have another wishlist with the same name"""
        user = self.context['request'].user
        if PropertyWishlist.objects.filter(user=user, name=value).exists():
            raise serializers.ValidationError("You already have a wishlist with this name")
        return value

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class PropertyWishlistUpdateSerializer(BaseSerializer):
    """Serializer for updating wishlists"""

    class Meta:
        model = PropertyWishlist
        fields = ['name', 'description', 'is_public']

    def validate_name(self, value):
        """Ensure user doesn't have another wishlist with the same name (excluding current)"""
        user = self.context['request'].user
        wishlist_id = self.instance.id if self.instance else None
        if PropertyWishlist.objects.filter(user=user, name=value).exclude(id=wishlist_id).exists():
            raise serializers.ValidationError("You already have a wishlist with this name")
        return value
