from rest_framework.routers import DefaultRouter
from .address import AddressViewSet
from .customuser import CustomUserViewSet
from .adminprofile import AdminProfileViewSet
from .buyerprofile import BuyerProfileViewSet
from .sellerprofile import SellerProfileViewSet
from .agentprofile import AgentProfileViewSet


router = DefaultRouter()
router.register(r'addresses', AddressViewSet)
router.register(r'users', CustomUserViewSet)
router.register(r'admin-profiles', AdminProfileViewSet)
router.register(r'buyer-profiles', BuyerProfileViewSet)
router.register(r'seller-profiles', SellerProfileViewSet)
router.register(r'agent-profiles', AgentProfileViewSet)