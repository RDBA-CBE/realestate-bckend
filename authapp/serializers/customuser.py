from authapp.models import CustomUser
from common.serializers import BaseSerializer


class CustomUserCreateSerializer(BaseSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"
        read_only_fields = ["created_by", "updated_by"]

class CustomUserListSerializer(BaseSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"
        read_only_fields = ["created_by", "updated_by"]

class CustomUserDetailSerializer(BaseSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"
        read_only_fields = ["created_by", "updated_by"]

class CustomUserUpdateSerializer(BaseSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"
        read_only_fields = ["created_by", "updated_by"]