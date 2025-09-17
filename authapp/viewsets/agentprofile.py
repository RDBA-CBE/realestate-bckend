from common.viewset import BaseViewSet
from rest_framework.permissions import IsAuthenticated
from authapp.models import AgentProfile
from authapp.serializers.agentprofile import (
    AgentProfileCreateSerializer,
    AgentProfileListSerializer,
    AgentProfileDetailSerializer,
    AgentProfileUpdateSerializer,
)

class AgentProfileViewSet(BaseViewSet):
    queryset = AgentProfile.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="Admin").exists():
            return AgentProfile.objects.all()
        return AgentProfile.objects.filter(created_by=user)

    def get_serializer_class(self):
        if self.action == "list":
            return AgentProfileListSerializer
        elif self.action == "retrieve":
            return AgentProfileDetailSerializer
        elif self.action == "create":
            return AgentProfileCreateSerializer
        elif self.action in ["update", "partial_update"]:
            return AgentProfileUpdateSerializer
        return AgentProfileDetailSerializer
    