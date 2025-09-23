from rest_framework import viewsets
from ..models.property import Project
from ..serializers import (
    ProjectListSerializer,
    ProjectDetailSerializer,
    ProjectCreateSerializer,
    ProjectUpdateSerializer
)
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = []  # Add appropriate permissions

    def get_serializer_class(self):
        if self.action == "list":
            return ProjectListSerializer
        elif self.action == "retrieve":
            return ProjectDetailSerializer
        elif self.action == "create":
            return ProjectCreateSerializer
        elif self.action in ["update", "partial_update"]:
            return ProjectUpdateSerializer
        return ProjectDetailSerializer


