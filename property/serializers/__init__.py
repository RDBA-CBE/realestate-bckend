from .amenity import (
    AmenityCreateSerializer,
    AmenityDetailSerializer,
    AmenityListSerializer,
    AmenityUpdateSerializer
)
from .property import (
    PropertyCreateSerializer,
    PropertyDetailSerializer,
    PropertyListSerializer,
    PropertyUpdateSerializer
)

from .propertyimage import (
    PropertyImageCreateSerializer,
    PropertyImageListSerializer,
    PropertyImageDetailSerializer,
    PropertyImageUpdateSerializer
)

from .propertytype import (
    PropertyTypeCreateSerializer,
    PropertyTypeDetailSerializer,
    PropertyTypeListSerializer,
    PropertyTypeUpdateSerializer
)
from .project import (
    ProjectCreateSerializer,
    ProjectDetailSerializer,
    ProjectListSerializer,
    ProjectUpdateSerializer
)

from .projectdocument import (
    ProjectDocumentCreateSerializer,
    ProjectDocumentDetailSerializer,    
    ProjectDocumentListSerializer,
    ProjectDocumentUpdateSerializer
)

from .projectphase import (
    ProjectPhaseCreateSerializer,
    ProjectPhaseDetailSerializer,
    ProjectPhaseListSerializer,
    ProjectPhaseUpdateSerializer
)

from .lead import (
    LeadCreateSerializer,
    LeadDetailSerializer,
    LeadListSerializer,
    LeadUpdateSerializer
)

from .floorplan import (
    FloorPlanCreateSerializer,
    FloorPlanDetailSerializer,
    FloorPlanListSerializer,
    FloorPlanUpdateSerializer
)

from .propertywishlist import (
    PropertyWishlistListSerializer,
    PropertyWishlistDetailSerializer,
    PropertyWishlistCreateSerializer,
    PropertyWishlistUpdateSerializer
)

__all__ = [ 
    'AmenityCreateSerializer',
    'AmenityDetailSerializer',
    'AmenityListSerializer',
    'AmenityUpdateSerializer',
    'PropertyCreateSerializer',
    'PropertyDetailSerializer',
    'PropertyListSerializer',
    'PropertyUpdateSerializer',
    'PropertyTypeCreateSerializer',
    'PropertyTypeDetailSerializer',
    'PropertyTypeListSerializer',
    'PropertyTypeUpdateSerializer',
    'ProjectCreateSerializer',
    'ProjectDetailSerializer',
    'ProjectListSerializer',
    'ProjectUpdateSerializer',
    'ProjectDocumentCreateSerializer',
    'ProjectDocumentDetailSerializer',
    'ProjectDocumentListSerializer',
    'ProjectDocumentUpdateSerializer',
    'PropertyImageCreateSerializer',
    'PropertyImageDetailSerializer',
    'PropertyImageListSerializer',
    'PropertyImageUpdateSerializer',
    'ProjectPhaseCreateSerializer',
    'ProjectPhaseDetailSerializer',
    'ProjectPhaseListSerializer',
    'ProjectPhaseUpdateSerializer',
    'LeadCreateSerializer',
    'LeadDetailSerializer',
    'LeadListSerializer',
    'LeadUpdateSerializer',
    'FloorPlanCreateSerializer',
    'FloorPlanDetailSerializer',
    'FloorPlanListSerializer',
    'FloorPlanUpdateSerializer',
]
