from common.viewset import BaseViewSet
from rest_framework.permissions import IsAuthenticated
from authapp.filters.customuser import CustomUserFilter
from authapp.models import CustomUser

from authapp.serializers.customuser import (
    CustomUserCreateSerializer,
    CustomUserListSerializer,
    CustomUserDetailSerializer,
    CustomUserUpdateSerializer,
)

class CustomUserViewSet(BaseViewSet):
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated]
    filterset_class = CustomUserFilter

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="Admin").exists():
            return CustomUser.objects.all()
        return CustomUser.objects.filter(created_by=user)

    def get_serializer_class(self):
        if self.action == "list":
            return CustomUserListSerializer
        elif self.action == "retrieve":
            return CustomUserDetailSerializer
        elif self.action == "create":
            return CustomUserCreateSerializer
        elif self.action in ["update", "partial_update"]:
            return CustomUserUpdateSerializer
        return CustomUserDetailSerializer

    
