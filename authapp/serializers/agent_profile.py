from rest_framework import serializers
from ..models.agentprofile import AgentProfile

class AgentProfileListSerializer(serializers.ModelSerializer):
    wishlist_id = serializers.SerializerMethodField()
    
    class Meta:
        model = AgentProfile
        fields = ['id', 'user', 'agency_name', 'wishlist_id']
    
    def get_wishlist_id(self, obj):
        """Return the wishlist ID for the user, if it exists"""
        from property.models import PropertyWishlist
        try:
            wishlist = PropertyWishlist.objects.get(created_by=obj.user)
            return wishlist.id
        except PropertyWishlist.DoesNotExist:
            return None

class AgentProfileDetailSerializer(serializers.ModelSerializer):
    wishlist_id = serializers.SerializerMethodField()
    
    class Meta:
        model = AgentProfile
        fields = '__all__'
    
    def get_wishlist_id(self, obj):
        """Return the wishlist ID for the user, if it exists"""
        from property.models import PropertyWishlist
        try:
            wishlist = PropertyWishlist.objects.get(created_by=obj.user)
            return wishlist.id
        except PropertyWishlist.DoesNotExist:
            return None

class AgentProfileCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgentProfile
        fields = ['user', 'agency_name']

class AgentProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgentProfile
        fields = ['agency_name']
