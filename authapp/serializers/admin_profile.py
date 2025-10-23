from rest_framework import serializers
from ..models.adminprofile import AdminProfile

class AdminProfileListSerializer(serializers.ModelSerializer):
    wishlist_id = serializers.SerializerMethodField()
    
    class Meta:
        model = AdminProfile
        fields = ['id', 'user', 'wishlist_id']
    
    def get_wishlist_id(self, obj):
        """Return the wishlist ID for the user, if it exists"""
        from property.models import PropertyWishlist
        try:
            wishlist = PropertyWishlist.objects.get(created_by=obj.user)
            return wishlist.id
        except PropertyWishlist.DoesNotExist:
            return None

class AdminProfileDetailSerializer(serializers.ModelSerializer):
    wishlist_id = serializers.SerializerMethodField()
    
    class Meta:
        model = AdminProfile
        fields = '__all__'
    
    def get_wishlist_id(self, obj):
        """Return the wishlist ID for the user, if it exists"""
        from property.models import PropertyWishlist
        try:
            wishlist = PropertyWishlist.objects.get(created_by=obj.user)
            return wishlist.id
        except PropertyWishlist.DoesNotExist:
            return None

class AdminProfileCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminProfile
        fields = '__all__' 

class AdminProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminProfile
        fields = '__all__'
        read_only_fields = ['id', 'user']
