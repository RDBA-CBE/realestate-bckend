from authapp.models import AdminProfile
from common.serializers import BaseSerializer


class AdminProfileCreateSerializer(BaseSerializer):
    class Meta:
        model = AdminProfile
        fields = "__all__"
        read_only_fields = ["created_by", "updated_by"]
        
class AdminProfileListSerializer(BaseSerializer):
    class Meta:
        model = AdminProfile
        fields = "__all__"
        read_only_fields = ["created_by", "updated_by"]

class AdminProfileDetailSerializer(BaseSerializer):
    class Meta:
        model = AdminProfile
        fields = "__all__"
        read_only_fields = ["created_by", "updated_by"]

class AdminProfileUpdateSerializer(BaseSerializer):
    class Meta:
        model = AdminProfile
        fields = "__all__"
        read_only_fields = ["created_by", "updated_by"]