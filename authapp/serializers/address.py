from authapp.models.address import Address
from common.serializers import BaseSerializer

class AddressCreateSerializer(BaseSerializer):
    class Meta:
        model = Address
        fields = "__all__"
        read_only_fields = ["created_by", "updated_by"]
        extra_kwargs = {
            "user": {"required": True},
            "street": {"required": True},
            "city": {"required": True},     
            "state": {"required": True},
            "country": {"required": True},
        }

class AddressListSerializer(BaseSerializer):
    class Meta:
        model = Address
        fields = "__all__"
        read_only_fields = ["created_by", "updated_by"]


class AddressDetailSerializer(BaseSerializer):
    class Meta:
        model = Address
        fields = "__all__"
        read_only_fields = ["created_by", "updated_by"]

class AddressUpdateSerializer(BaseSerializer):
    class Meta:
        model = Address
        fields = "__all__"
        read_only_fields = ["created_by", "updated_by"]
        extra_kwargs = {
            "user": {"required": False},
            "street": {"required": False},
            "city": {"required": False},     
            "state": {"required": False},
            "country": {"required": False},
        }