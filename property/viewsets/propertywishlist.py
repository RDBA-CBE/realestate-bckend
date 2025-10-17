from rest_framework.permissions import IsAuthenticated
from django.db import models
from django_filters import rest_framework as filters
from common.paginator import Pagination
from common.viewset import BaseViewSet
from ..filters import PropertyWishlistFilter
from ..models import PropertyWishlist
from ..serializers.propertywishlist import (
    PropertyWishlistListSerializer,
    PropertyWishlistDetailSerializer,
    PropertyWishlistCreateSerializer,
    PropertyWishlistUpdateSerializer
)






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
            models.Q(created_by=self.request.user) | models.Q(is_public=True)
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

    # def perform_create(self, serializer):
    #     """Set the user when creating wishlists"""
    #     serializer.save(user=self.request.user)