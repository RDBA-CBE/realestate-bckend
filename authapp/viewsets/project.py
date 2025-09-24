from rest_framework import viewsets
from common.paginator import Pagination
from ..models.property import Project
from authapp.filters import ProjectFilter
from ..serializers import (
    ProjectListSerializer,
    ProjectDetailSerializer,
    ProjectCreateSerializer,
    ProjectUpdateSerializer
)
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete']
    filterset_class = ProjectFilter
    pagination_class = Pagination
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


