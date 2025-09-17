from authapp.models import AgentProfile
from common.serializers import BaseSerializer

class AgentProfileCreateSerializer(BaseSerializer):
    class Meta:
        model = AgentProfile
        fields = "__all__"
        read_only_fields = ["created_by", "updated_by"]
        extra_kwargs = {
            "user": {"required": True},
            "phone_number": {"required": True},
            "address": {"required": True},
            "license_number": {"required": True},
        }

class AgentProfileListSerializer(BaseSerializer):
    class Meta:
        model = AgentProfile
        fields = "__all__"
        read_only_fields = ["created_by", "updated_by"]

class AgentProfileDetailSerializer(BaseSerializer):
    class Meta:
        model = AgentProfile
        fields = "__all__"
        read_only_fields = ["created_by", "updated_by"]

class AgentProfileUpdateSerializer(BaseSerializer):
    class Meta:
        model = AgentProfile
        fields = "__all__"
        read_only_fields = ["created_by", "updated_by"]
        extra_kwargs = {
            "user": {"required": False},
            "phone_number": {"required": False},
            "address": {"required": False},
            "license_number": {"required": False},
        }
        