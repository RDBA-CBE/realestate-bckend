from rest_framework import serializers
from ..models.buyerprofile import BuyerProfile

class BuyerProfileListSerializer(serializers.ModelSerializer):
    wishlist_id = serializers.SerializerMethodField()
    
    class Meta:
        model = BuyerProfile
        fields = '__all__'
    
    def get_wishlist_id(self, obj):
        """Return the wishlist ID for the user, if it exists"""
        from property.models import PropertyWishlist
        try:
            wishlist = PropertyWishlist.objects.get(created_by=obj.user)
            return wishlist.id
        except PropertyWishlist.DoesNotExist:
            return None

class BuyerProfileDetailSerializer(serializers.ModelSerializer):
    wishlist_id = serializers.SerializerMethodField()
    
    class Meta:
        model = BuyerProfile
        fields = '__all__'
    
    def get_wishlist_id(self, obj):
        """Return the wishlist ID for the user, if it exists"""
        from property.models import PropertyWishlist
        try:
            wishlist = PropertyWishlist.objects.get(created_by=obj.user)
            return wishlist.id
        except PropertyWishlist.DoesNotExist:
            return None

class BuyerProfileCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuyerProfile
        fields = "__all__"

class BuyerProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuyerProfile
        fields = "__all__"
