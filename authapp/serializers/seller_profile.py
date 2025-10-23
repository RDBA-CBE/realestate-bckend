from rest_framework import serializers
from authapp.models  import SellerProfile
from common.serializers import BaseSerializer

class SellerProfileCreateSerializer(BaseSerializer):
    class Meta:
        model = SellerProfile
        fields = "__all__"
        read_only_fields = ["created_by", "updated_by"]


class SellerProfileListSerializer(BaseSerializer):
    wishlist_id = serializers.SerializerMethodField()
    
    class Meta:
        model = SellerProfile
        fields = "__all__"
        read_only_fields = ["created_by", "updated_by"]
    
    def get_wishlist_id(self, obj):
        """Return the wishlist ID for the user, if it exists"""
        from property.models import PropertyWishlist
        try:
            wishlist = PropertyWishlist.objects.get(created_by=obj.user)
            return wishlist.id
        except PropertyWishlist.DoesNotExist:
            return None


class SellerProfileDetailSerializer(BaseSerializer):
    wishlist_id = serializers.SerializerMethodField()
    
    class Meta:
        model = SellerProfile
        fields = "__all__"
        read_only_fields = ["created_by", "updated_by"]
    
    def get_wishlist_id(self, obj):
        """Return the wishlist ID for the user, if it exists"""
        from property.models import PropertyWishlist
        try:
            wishlist = PropertyWishlist.objects.get(created_by=obj.user)
            return wishlist.id
        except PropertyWishlist.DoesNotExist:
            return None

class SellerProfileUpdateSerializer(BaseSerializer):
    class Meta:
        model = SellerProfile
        fields = "__all__"
        read_only_fields = ["created_by", "updated_by"]
