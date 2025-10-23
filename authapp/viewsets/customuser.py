from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from common.paginator import Pagination
from authapp.filters import CustomUserFilter
from authapp.models import CustomUser

from authapp.serializers.customuser import (
    CustomUserCreateSerializer,
    CustomUserListSerializer,
    CustomUserDetailSerializer,
    CustomUserUpdateSerializer,
)

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated]
    http_method_names = ['post', 'get', 'patch', 'delete']
    filterset_class = CustomUserFilter
    pagination_class = Pagination

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="Admin").exists():
            return CustomUser.objects.exclude(id=user.id)
        return (CustomUser.objects.exclude(id=user.id).exclude(groups__name="Admin"))

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

    
