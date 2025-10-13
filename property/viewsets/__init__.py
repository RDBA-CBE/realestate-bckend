from .amenity import AmenityViewSet
from .property import PropertyViewSet
from .propertytype import PropertyTypeViewSet
from .project import ProjectViewSet 
from .propertyimage import PropertyImageViewSet
from .projectdocument import ProjectDocumentViewSet
from .projectphase import ProjectPhaseViewSet
from .lead import LeadViewSet


__all__ = [
    'AmenityViewSet',
    'PropertyViewSet',
    'PropertyTypeViewSet',
    'ProjectViewSet',
    'PropertyImageViewSet',
    'ProjectDocumentViewSet',
    'ProjectPhaseViewSet',
    'LeadViewSet',
]