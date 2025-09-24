from rest_framework import viewsets
from common.paginator import Pagination
from property.models import ProjectDocument
from property.serializers import (
    ProjectDocumentListSerializer,
    ProjectDocumentDetailSerializer,
    ProjectDocumentCreateSerializer,
    ProjectDocumentUpdateSerializer,
)

class ProjectDocumentViewSet(viewsets.ModelViewSet):
    queryset = ProjectDocument.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete']
    pagination_class = Pagination

    def get_serializer_class(self):
        if self.action == "list":
            return ProjectDocumentListSerializer
        elif self.action == "retrieve":
            return ProjectDocumentDetailSerializer
        elif self.action == "create":
            return ProjectDocumentCreateSerializer
        elif self.action in ["update", "partial_update"]:
            return ProjectDocumentUpdateSerializer
        return ProjectDocumentDetailSerializer


