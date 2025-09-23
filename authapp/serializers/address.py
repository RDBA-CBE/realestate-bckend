from authapp.models import Address
from common.serializers import BaseSerializer

class AddressCreateSerializer(BaseSerializer):
    class Meta:
        model = Address
        fields = "__all__"
        read_only_fields = ["created_by", "updated_by"]

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