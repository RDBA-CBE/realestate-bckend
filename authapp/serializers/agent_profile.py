from authapp.models import AgentProfile
from common.serializers import BaseSerializer

class AgentProfileCreateSerializer(BaseSerializer):
    class Meta:
        model = AgentProfile
        fields = "__all__"
        read_only_fields = ["created_by", "updated_by"]

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

        