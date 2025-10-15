from rest_framework import serializers
from common.serializers import BaseSerializer
from ..models import PropertyFavorite, PropertyWishlist, PropertyWishlistItem, Property
from .property import PropertyListSerializer


class PropertyFavoriteListSerializer(BaseSerializer):
    """Serializer for listing user's favorite properties"""
    property = PropertyListSerializer(read_only=True)

    class Meta:
        model = PropertyFavorite
        fields = ['id', 'property', 'notes', 'created_at']


class PropertyFavoriteDetailSerializer(BaseSerializer):
    """Serializer for detailed favorite property view"""
    property = PropertyListSerializer(read_only=True)

    class Meta:
        model = PropertyFavorite
        fields = ['id', 'user', 'property', 'notes', 'created_at', 'updated_at']


class PropertyFavoriteCreateSerializer(BaseSerializer):
    """Serializer for creating favorite properties"""

    class Meta:
        model = PropertyFavorite
        fields = ['property', 'notes']

    def validate_property(self, value):
        """Ensure user doesn't already have this property in favorites"""
        user = self.context['request'].user
        if PropertyFavorite.objects.filter(user=user, property=value).exists():
            raise serializers.ValidationError("This property is already in your favorites")
        return value

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


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


class PropertyWishlistItemSerializer(BaseSerializer):
    """Serializer for wishlist items"""
    property = PropertyListSerializer(read_only=True)
    wishlist = PropertyWishlistListSerializer(read_only=True)

    class Meta:
        model = PropertyWishlistItem
        fields = ['id', 'wishlist', 'property', 'notes', 'order', 'created_at', 'updated_at']


class PropertyWishlistItemCreateSerializer(BaseSerializer):
    """Serializer for creating wishlist items"""
    
    def __init__(self, *args, **kwargs):
        self.wishlist = kwargs.pop('wishlist', None)
        super().__init__(*args, **kwargs)

    class Meta:
        model = PropertyWishlistItem
        fields = ['property', 'notes', 'order']

    def validate_property(self, value):
        """Ensure property isn't already in the wishlist"""
        if self.wishlist and PropertyWishlistItem.objects.filter(
            wishlist=self.wishlist, 
            property=value
        ).exists():
            raise serializers.ValidationError("This property is already in the wishlist")
        return value

    def create(self, validated_data):
        if self.wishlist:
            validated_data['wishlist'] = self.wishlist
        return super().create(validated_data)


class PropertyWishlistItemUpdateSerializer(BaseSerializer):
    """Serializer for updating wishlist items"""

    class Meta:
        model = PropertyWishlistItem
        fields = ['notes', 'order']