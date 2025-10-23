from django.urls import path, include
from rest_framework.routers import DefaultRouter
from authapp.viewsets import (
    AddressViewSet,
    CustomUserViewSet,
    AdminProfileViewSet,
    BuyerProfileViewSet,
    SellerProfileViewSet,
    AgentProfileViewSet,
    AuthViewSet,
    PasswordResetViewSet,
    RegistrationViewSet,
    GroupViewSet,
)

router = DefaultRouter()

router.register(r'addresses', AddressViewSet, basename="addresses")
router.register(r'users', CustomUserViewSet, basename="users")
router.register(r'admin-profiles', AdminProfileViewSet, basename="admin-profiles")
router.register(r'buyer-profiles', BuyerProfileViewSet, basename="buyer-profiles")
router.register(r'seller-profiles', SellerProfileViewSet, basename="seller-profiles")
router.register(r'agent-profiles', AgentProfileViewSet, basename="agent-profiles")
router.register(r'authentication', AuthViewSet, basename="authentication")
router.register(r'password-reset', PasswordResetViewSet, basename="password-reset")
router.register(r'register', RegistrationViewSet, basename="register")
router.register(r'groups', GroupViewSet, basename="groups")

urlpatterns = [
    path('', include(router.urls)),
    path('', include('property.urls')),
]
