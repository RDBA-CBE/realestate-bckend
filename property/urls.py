from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets.property import PropertyViewSet
from .viewsets.project import ProjectViewSet
from .viewsets.propertytype import PropertyTypeViewSet
from .viewsets.amenity import AmenityViewSet
from .viewsets.propertyimage import PropertyImageViewSet
from .viewsets.propertyvideo import PropertyVideoViewSet
from .viewsets.virtualtour import VirtualTourViewSet
from .viewsets.lead import LeadViewSet
from .viewsets.floorplan import FloorPlanViewSet

router = DefaultRouter()
router.register(r'properties', PropertyViewSet, basename="properties")
router.register(r'projects', ProjectViewSet, basename="projects")
router.register(r'property-types', PropertyTypeViewSet, basename="property-types")
router.register(r'amenities', AmenityViewSet, basename="amenities")
router.register(r'property-images', PropertyImageViewSet, basename="property-images")
router.register(r'property-videos', PropertyVideoViewSet, basename="property-videos")
router.register(r'virtual-tours', VirtualTourViewSet, basename="virtual-tours")
router.register(r'leads', LeadViewSet, basename="leads")
router.register(r'floor-plans', FloorPlanViewSet, basename="floor-plans")

urlpatterns = [
    path('', include(router.urls)),
]