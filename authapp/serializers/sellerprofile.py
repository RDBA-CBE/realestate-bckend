from authapp.models  import SellerProfile
from common.serializers import BaseSerializer

class SellerProfileCreateSerializer(BaseSerializer):
    class Meta:
        model = SellerProfile
        fields = "__all__"
        read_only_fields = ["created_by", "updated_by"]


class SellerProfileListSerializer(BaseSerializer):
    class Meta:
        model = SellerProfile
        fields = "__all__"
        read_only_fields = ["created_by", "updated_by"]


class SellerProfileDetailSerializer(BaseSerializer):
    class Meta:
        model = SellerProfile
        fields = "__all__"
        read_only_fields = ["created_by", "updated_by"]

class SellerProfileUpdateSerializer(BaseSerializer):
    class Meta:
        model = SellerProfile
        fields = "__all__"
        read_only_fields = ["created_by", "updated_by"]
