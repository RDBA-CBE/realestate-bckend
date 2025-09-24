from common.viewset import BaseViewSet
from rest_framework.permissions import IsAuthenticated
from common.paginator import Pagination
from authapp.filters import SellerProfileFilter
from authapp.models import SellerProfile
from authapp.serializers import (
    SellerProfileCreateSerializer,
    SellerProfileListSerializer,
    SellerProfileDetailSerializer,
    SellerProfileUpdateSerializer,
)

class SellerProfileViewSet(BaseViewSet):
    queryset = SellerProfile.objects.all()
    permission_classes = [IsAuthenticated]
    filterset_class = SellerProfileFilter
    pagination_class = Pagination

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="Admin").exists():
            return SellerProfile.objects.all()
        return SellerProfile.objects.filter(created_by=user)

    def get_serializer_class(self):
        if self.action == "list":
            return SellerProfileListSerializer
        elif self.action == "retrieve":
            return SellerProfileDetailSerializer
        elif self.action == "create":
            return SellerProfileCreateSerializer
        elif self.action in ["update", "partial_update"]:
            return SellerProfileUpdateSerializer
        return SellerProfileDetailSerializer
    
