from rest_framework import viewsets
from common.paginator import Pagination
from property.models import ProjectPhase
from property.serializers import (
    ProjectPhaseListSerializer,
    ProjectPhaseDetailSerializer,
    ProjectPhaseCreateSerializer,
    ProjectPhaseUpdateSerializer,
)

class ProjectPhaseViewSet(viewsets.ModelViewSet):
    queryset = ProjectPhase.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete']
    pagination_class = Pagination

    def get_serializer_class(self):
        if self.action == "list":
            return ProjectPhaseListSerializer
        elif self.action == "retrieve":
            return ProjectPhaseDetailSerializer
        elif self.action == "create":
            return ProjectPhaseCreateSerializer
        elif self.action in ["update", "partial_update"]:
            return ProjectPhaseUpdateSerializer
        return ProjectPhaseDetailSerializer

