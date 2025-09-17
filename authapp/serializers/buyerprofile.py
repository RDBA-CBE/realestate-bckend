from authapp.models import BuyerProfile
from common.serializers import BaseSerializer


class BuyerProfileCreateSerializer(BaseSerializer):
    class Meta:
        model = BuyerProfile
        fields = "__all__"
        read_only_fields = ["created_by", "updated_by"]
        extra_kwargs = {
            "user": {"required": True},
            "phone_number": {"required": True},
            "address": {"required": True},
        }

class BuyerProfileListSerializer(BaseSerializer):
    class Meta:
        model = BuyerProfile
        fields = "__all__"
        read_only_fields = ["created_by", "updated_by"]
        
class BuyerProfileDetailSerializer(BaseSerializer):
    class Meta:
        model = BuyerProfile
        fields = "__all__"
        read_only_fields = ["created_by", "updated_by"]

class BuyerProfileUpdateSerializer(BaseSerializer):
    class Meta:
        model = BuyerProfile
        fields = "__all__"
        read_only_fields = ["created_by", "updated_by"]
        extra_kwargs = {
            "user": {"required": False},
            "phone_number": {"required": False},
            "address": {"required": False},
        }