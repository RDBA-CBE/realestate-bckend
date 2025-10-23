from rest_framework.permissions import IsAuthenticated
from django.db import models
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from common.paginator import Pagination
from common.viewset import BaseViewSet
from ..filters import PropertyWishlistFilter
from ..models import PropertyWishlist, Property
from ..serializers.propertywishlist import (
    PropertyWishlistListSerializer,
    PropertyWishlistDetailSerializer,
    PropertyWishlistCreateSerializer,
    PropertyWishlistUpdateSerializer,
    AddPropertyToWishlistSerializer,
    RemovePropertyFromWishlistSerializer
)






class PropertyWishlistViewSet(BaseViewSet):
    """ViewSet for managing property wishlist (one per user)"""
    queryset = PropertyWishlist.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete']
    filterset_class = PropertyWishlistFilter
    pagination_class = Pagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return only the authenticated user's wishlist"""
        return self.queryset.filter(created_by=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return PropertyWishlistListSerializer
        elif self.action == "create":
            return PropertyWishlistCreateSerializer
        elif self.action == "retrieve":
            return PropertyWishlistDetailSerializer
        elif self.action in ["update", "partial_update"]:
            return PropertyWishlistUpdateSerializer
        elif self.action == "add_property":
            return AddPropertyToWishlistSerializer
        elif self.action == "remove_property":
            return RemovePropertyFromWishlistSerializer
        elif self.action == "my_wishlist":
            return PropertyWishlistDetailSerializer
        return PropertyWishlistDetailSerializer

    @action(detail=False, methods=['post'], url_path='add-property', serializer_class=AddPropertyToWishlistSerializer)
    def add_property(self, request):
        """Add a property to the user's wishlist. Creates wishlist if it doesn't exist."""
        serializer = AddPropertyToWishlistSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        property_id = serializer.validated_data['property_id']
        property_obj = Property.objects.get(id=property_id)
        
        # Get or create the user's wishlist
        wishlist, created = PropertyWishlist.objects.get_or_create(
            created_by=request.user,
            defaults={
                'name': 'My Wishlist',
                'description': 'My favorite properties'
            }
        )
        
        # Check if property is already in wishlist
        if wishlist.properties.filter(id=property_id).exists():
            return Response({
                "message": "Property is already in your wishlist.",
                "wishlist_id": wishlist.id,
                "property_id": property_id
            }, status=status.HTTP_200_OK)
        
        # Add the property to wishlist
        wishlist.properties.add(property_obj)
        
        return Response({
            "message": "Property added to wishlist successfully.",
            "wishlist_id": wishlist.id,
            "property_id": property_id,
            "total_properties": wishlist.property_count
        }, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='remove-property', serializer_class=RemovePropertyFromWishlistSerializer)
    def remove_property(self, request):
        """Remove a property from the user's wishlist."""
        serializer = RemovePropertyFromWishlistSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        property_id = serializer.validated_data['property_id']
        
        # Get the user's wishlist
        try:
            wishlist = PropertyWishlist.objects.get(created_by=request.user)
        except PropertyWishlist.DoesNotExist:
            return Response({
                "error": "You don't have a wishlist yet."
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Check if property is in wishlist
        if not wishlist.properties.filter(id=property_id).exists():
            return Response({
                "error": "Property is not in your wishlist."
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Remove the property
        property_obj = Property.objects.get(id=property_id)
        wishlist.properties.remove(property_obj)
        
        return Response({
            "message": "Property removed from wishlist successfully.",
            "wishlist_id": wishlist.id,
            "property_id": property_id,
            "total_properties": wishlist.property_count
        }, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'], url_path='my-wishlist')
    def my_wishlist(self, request):
        """Get the authenticated user's wishlist with all properties."""
        try:
            wishlist = PropertyWishlist.objects.get(created_by=request.user)
            serializer = PropertyWishlistDetailSerializer(wishlist, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except PropertyWishlist.DoesNotExist:
            return Response({
                "message": "You don't have a wishlist yet. Add properties to create one.",
                "wishlist": None
            }, status=status.HTTP_200_OK)