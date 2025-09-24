from common.viewset import BaseViewSet
from rest_framework.permissions import IsAuthenticated
from common.paginator import Pagination
from authapp.filters import AgentProfileFilter
from authapp.models import AgentProfile
from authapp.serializers.agent_profile import (
    AgentProfileCreateSerializer,
    AgentProfileListSerializer,
    AgentProfileDetailSerializer,
    AgentProfileUpdateSerializer,
)

class AgentProfileViewSet(BaseViewSet):
    queryset = AgentProfile.objects.all()
    permission_classes = [IsAuthenticated]
    filterset_class = AgentProfileFilter
    pagination_class = Pagination

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
    