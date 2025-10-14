from rest_framework import viewsets
from common.viewset import BaseViewSet
from common.paginator import Pagination
from ..models import Project
from ..filters.project import ProjectFilter
from ..serializers.project import (
    ProjectListSerializer,
    ProjectDetailSerializer,
    ProjectCreateSerializer,
    ProjectUpdateSerializer
)
class ProjectViewSet(BaseViewSet):
    queryset = Project.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete']
    filterset_class = ProjectFilter
    pagination_class = Pagination
    permission_classes = []  # Add appropriate permissions
    order_by = ['-id']  

    def get_queryset(self):
        queryset = super().get_queryset()
        # Only show approved projects to non-admin users
        if not self.request.user.groups.filter(name='Admin').exists():
            queryset = queryset.filter(is_approved=True)
        return queryset

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