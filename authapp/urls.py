from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets.views import RegistrationAPIView, LoginAPIView, UserProfileAPIView, AdminUserViewSet

router = DefaultRouter()
router.register(r'users', AdminUserViewSet)

urlpatterns = [
    path('register/', RegistrationAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('profile/', UserProfileAPIView.as_view(), name='profile'),
    path('admin/', include(router.urls)),
]