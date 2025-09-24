from authapp.models import CustomUser
from common.serializers import BaseSerializer


class CustomUserCreateSerializer(BaseSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"

class CustomUserListSerializer(BaseSerializer):
    class Meta:
        model = CustomUser
        exclude = ['password', 'last_login', 'is_superuser', 'is_staff', 'is_active', 'date_joined']

class CustomUserDetailSerializer(BaseSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"

class CustomUserUpdateSerializer(BaseSerializer):
    class Meta:
        model = CustomUser
        exclude = ['last_login', 'is_superuser', 'is_staff', 'is_active', 'date_joined']