from rest_framework import serializers
from ..models.developerprofile import DeveloperProfile

class DeveloperProfileListSerializer(serializers.ModelSerializer):
    wishlist_id = serializers.SerializerMethodField()
    
    class Meta:
        model = DeveloperProfile
        fields = ['id', 'user', 'company_name', 'wishlist_id']
    
    def get_wishlist_id(self, obj):
        """Return the wishlist ID for the user, if it exists"""
        from property.models import PropertyWishlist
        try:
            wishlist = PropertyWishlist.objects.get(created_by=obj.user)
            return wishlist.id
        except PropertyWishlist.DoesNotExist:
            return None

class DeveloperProfileDetailSerializer(serializers.ModelSerializer):
    wishlist_id = serializers.SerializerMethodField()
    
    class Meta:
        model = DeveloperProfile
        fields = '__all__'
    
    def get_wishlist_id(self, obj):
        """Return the wishlist ID for the user, if it exists"""
        from property.models import PropertyWishlist
        try:
            wishlist = PropertyWishlist.objects.get(created_by=obj.user)
            return wishlist.id
        except PropertyWishlist.DoesNotExist:
            return None

class DeveloperProfileCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeveloperProfile
        fields = ['user', 'company_name']

class DeveloperProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeveloperProfile
        fields = ['company_name']
