from common.viewset import BaseViewSet
from rest_framework.permissions import IsAuthenticated
from authapp.models import Address, CustomUser
from authapp.filters.address import AddressFilter
from authapp.serializers.address import (
    AddressCreateSerializer,
    AddressListSerializer,
    AddressDetailSerializer,
    AddressUpdateSerializer,
)

class AddressViewSet(BaseViewSet):
    queryset = Address.objects.all()
    permission_classes = [IsAuthenticated]
    filterset_class = AddressFilter

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="Admin").exists():
            return CustomUser.objects.all()
        return CustomUser.objects.filter(created_by=user)

    def get_serializer_class(self):
        if self.action == "list":
            return AddressListSerializer
        elif self.action == "retrieve":
            return AddressDetailSerializer
        elif self.action == "create":
            return AddressCreateSerializer
        elif self.action in ["update", "partial_update"]:
            return AddressUpdateSerializer
        return AddressDetailSerializer
