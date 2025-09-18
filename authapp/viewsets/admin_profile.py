from common.viewset import BaseViewSet
from rest_framework.permissions import IsAuthenticated
from authapp.filters.admin_profile import AdminProfileFilter
from authapp.serializers import (
    AdminProfileCreateSerializer,
    AdminProfileListSerializer,
    AdminProfileDetailSerializer,
    AdminProfileUpdateSerializer,
)
from authapp.models import AdminProfile

class AdminProfileViewSet(BaseViewSet):
    queryset = AdminProfile.objects.all()
    permission_classes = [IsAuthenticated]
    filterset_class = AdminProfileFilter

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="Admin").exists():
            return AdminProfile.objects.all()
        return AdminProfile.objects.filter(created_by=user)

    def get_serializer_class(self):
        if self.action == "list":
            return AdminProfileListSerializer
        elif self.action == "retrieve":
            return AdminProfileDetailSerializer
        elif self.action == "create":
            return AdminProfileCreateSerializer
        elif self.action in ["update", "partial_update"]:
            return AdminProfileUpdateSerializer
        return AdminProfileDetailSerializer
    
