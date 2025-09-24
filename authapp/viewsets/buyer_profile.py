from common.viewset import BaseViewSet
from rest_framework.permissions import IsAuthenticated
from common.paginator import Pagination
from authapp.filters import BuyerProfileFilter
from authapp.models import BuyerProfile
from authapp.serializers import (
    BuyerProfileCreateSerializer,
    BuyerProfileListSerializer,
    BuyerProfileDetailSerializer,
    BuyerProfileUpdateSerializer,
)

class BuyerProfileViewSet(BaseViewSet):
    queryset = BuyerProfile.objects.all()
    permission_classes = [IsAuthenticated]
    filterset_class = BuyerProfileFilter
    pagination_class = Pagination

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="Admin").exists():
            return BuyerProfile.objects.all()
        return BuyerProfile.objects.filter(created_by=user)
    
    def get_serializer_class(self):
        if self.action == "list":
            return BuyerProfileListSerializer
        elif self.action == "retrieve":
            return BuyerProfileDetailSerializer
        elif self.action == "create":
            return BuyerProfileCreateSerializer
        elif self.action in ["update", "partial_update"]:
            return BuyerProfileUpdateSerializer
        return BuyerProfileDetailSerializer

