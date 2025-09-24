from django.urls import path, include
from rest_framework.routers import DefaultRouter
from property.viewsets import (
    PropertyViewSet, ProjectViewSet, PropertyTypeViewSet, 
    AmenityViewSet, PropertyImageViewSet, ProjectDocumentViewSet,
    ProjectPhaseViewSet
)

router = DefaultRouter()
router.register(r'properties', PropertyViewSet, basename="properties")
router.register(r'projects', ProjectViewSet, basename="projects")
router.register(r'property-images', PropertyImageViewSet, basename="property-images")
router.register(r'project-documents', ProjectDocumentViewSet, basename="project-documents")
router.register(r'property-types', PropertyTypeViewSet, basename="property-types")
router.register(r'amenities', AmenityViewSet, basename="amenities")
router.register(r'project-phases', ProjectPhaseViewSet, basename="project-phases")


urlpatterns = [
    path('', include(router.urls)),
]