from django.urls import path, include
from rest_framework.routers import DefaultRouter
from authapp.viewsets import (
    AddressViewSet,
    CustomUserViewSet,
    AdminProfileViewSet,
    BuyerProfileViewSet,
    SellerProfileViewSet,
    AgentProfileViewSet,
)

router = DefaultRouter()

router.register(r'addresses', AddressViewSet)
router.register(r'users', CustomUserViewSet)
router.register(r'admin-profiles', AdminProfileViewSet)
router.register(r'buyer-profiles', BuyerProfileViewSet)
router.register(r'seller-profiles', SellerProfileViewSet)
router.register(r'agent-profiles', AgentProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
