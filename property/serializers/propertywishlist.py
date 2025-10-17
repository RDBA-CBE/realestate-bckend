from rest_framework import serializers
from common.serializers import BaseSerializer
from ..models import PropertyWishlist
from .property import PropertyListSerializer



class PropertyWishlistListSerializer(BaseSerializer):
    """Serializer for listing user's wishlists"""
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
    """Serializer for creating wishlists"""

    class Meta:
        model = PropertyWishlist
        fields = '__all__'


class PropertyWishlistUpdateSerializer(BaseSerializer):
    """Serializer for updating wishlists"""

    class Meta:
        model = PropertyWishlist
        fields = "__all__"

    def validate_name(self, value):
        """Ensure user doesn't have another wishlist with the same name (excluding current)"""
        user = self.context['request'].user
        wishlist_id = self.instance.id if self.instance else None
        if PropertyWishlist.objects.filter(created_by=user, name=value).exclude(id=wishlist_id).exists():
            raise serializers.ValidationError("You already have a wishlist with this name")
        return value
