from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from django.db import models
from django_filters import rest_framework as filters
from common.paginator import Pagination
from common.viewset import BaseViewSet
from ..models import PropertyFavorite, PropertyWishlist, PropertyWishlistItem
from ..serializers.propertyfavorite import (
    PropertyFavoriteListSerializer,
    PropertyFavoriteCreateSerializer,
    PropertyFavoriteDetailSerializer,
    PropertyWishlistListSerializer,
    PropertyWishlistDetailSerializer,
    PropertyWishlistCreateSerializer,
    PropertyWishlistUpdateSerializer,
    PropertyWishlistItemSerializer,
    PropertyWishlistItemCreateSerializer,
    PropertyWishlistItemUpdateSerializer,
)


class PropertyFavoriteFilter(filters.FilterSet):
    """Filter for property favorites"""
    property = filters.NumberFilter(field_name='property__id')
    created_after = filters.DateFilter(field_name='created_at', lookup_expr='gte')
    created_before = filters.DateFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = PropertyFavorite
        fields = ['property']


class PropertyFavoriteViewSet(BaseViewSet):
    """ViewSet for managing property favorites"""
    queryset = PropertyFavorite.objects.all()
    http_method_names = ['get', 'post', 'delete']
    filterset_class = PropertyFavoriteFilter
    pagination_class = Pagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return only current user's favorites"""
        return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return PropertyFavoriteListSerializer
        elif self.action == "create":
            return PropertyFavoriteCreateSerializer
        elif self.action == "retrieve":
            return PropertyFavoriteDetailSerializer
        return PropertyFavoriteDetailSerializer

    def perform_create(self, serializer):
        """Set the user when creating favorites"""
        serializer.save(user=self.request.user)


class PropertyWishlistFilter(filters.FilterSet):
    """Filter for property wishlists"""
    is_public = filters.BooleanFilter()
    created_after = filters.DateFilter(field_name='created_at', lookup_expr='gte')
    created_before = filters.DateFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = PropertyWishlist
        fields = ['is_public']


class PropertyWishlistViewSet(BaseViewSet):
    """ViewSet for managing property wishlists"""
    queryset = PropertyWishlist.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete']
    filterset_class = PropertyWishlistFilter
    pagination_class = Pagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return user's wishlists and public wishlists from other users"""
        return self.queryset.filter(
            models.Q(user=self.request.user) | models.Q(is_public=True)
        ).distinct()

    def get_serializer_class(self):
        if self.action == "list":
            return PropertyWishlistListSerializer
        elif self.action == "create":
            return PropertyWishlistCreateSerializer
        elif self.action == "retrieve":
            return PropertyWishlistDetailSerializer
        elif self.action in ["update", "partial_update"]:
            return PropertyWishlistUpdateSerializer
        return PropertyWishlistDetailSerializer

    def perform_create(self, serializer):
        """Set the user when creating wishlists"""
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'], url_path='add-property')
    def add_property(self, request, pk=None):
        """Add a property to a wishlist"""
        wishlist = self.get_object()

        # Check if user owns this wishlist
        if wishlist.user != request.user:
            return Response(
                {"error": "You can only modify your own wishlists"},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = PropertyWishlistItemCreateSerializer(
            data=request.data,
            wishlist=wishlist
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'], url_path=r'remove-property/(?P<property_id>\d+)')
    def remove_property(self, request, pk=None, property_id=None):
        """Remove a property from a wishlist"""
        wishlist = self.get_object()

        # Check if user owns this wishlist
        if wishlist.user != request.user:
            return Response(
                {"error": "You can only modify your own wishlists"},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            item = PropertyWishlistItem.objects.get(
                wishlist=wishlist,
                property_id=property_id
            )
            item.delete()
            return Response(
                {"success": "Property removed from wishlist"},
                status=status.HTTP_200_OK
            )
        except PropertyWishlistItem.DoesNotExist:
            return Response(
                {"error": "Property not found in this wishlist"},
                status=status.HTTP_404_NOT_FOUND
            )


class PropertyWishlistItemViewSet(BaseViewSet):
    """ViewSet for managing wishlist items"""
    queryset = PropertyWishlistItem.objects.all()
    http_method_names = ['get', 'patch', 'delete']
    pagination_class = Pagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return only items from user's wishlists"""
        return self.queryset.filter(wishlist__user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return PropertyWishlistItemSerializer
        elif self.action == "retrieve":
            return PropertyWishlistItemSerializer
        elif self.action in ["update", "partial_update"]:
            return PropertyWishlistItemUpdateSerializer
        return PropertyWishlistItemSerializer

    def perform_update(self, serializer):
        """Ensure user owns the wishlist before updating"""
        if serializer.instance.wishlist.user != self.request.user:
            raise serializers.ValidationError("You can only modify items in your own wishlists")
        serializer.save()