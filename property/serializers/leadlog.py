from rest_framework import serializers
from common.serializers import BaseSerializer
from ..models import LeadLog, Lead
from authapp.serializers.customuser import CustomUserListSerializer


class LeadLogListSerializer(BaseSerializer):
    """Simple serializer for listing lead logs"""
    performed_by = CustomUserListSerializer(read_only=True)
    action_display = serializers.CharField(source='get_action_display', read_only=True)
    lead_name = serializers.SerializerMethodField()

    class Meta:
        model = LeadLog
        fields = [
            'id', 'action', 'action_display', 'lead', 'lead_name',
            'performed_by', 'old_value', 'new_value', 'description',
            'notes', 'created_at'
        ]

    def get_lead_name(self, obj):
        return obj.lead.full_name if obj.lead else None


class LeadLogDetailSerializer(BaseSerializer):
    """Simple serializer for detailed lead log view"""
    performed_by = CustomUserListSerializer(read_only=True)
    action_display = serializers.CharField(source='get_action_display', read_only=True)
    lead_details = serializers.SerializerMethodField()

    class Meta:
        model = LeadLog
        fields = [
            'id', 'action', 'action_display', 'lead', 'lead_details',
            'performed_by', 'old_value', 'new_value', 'description',
            'notes', 'created_at', 'updated_at'
        ]

    def get_lead_details(self, obj):
        if obj.lead:
            return {
                'id': obj.lead.id,
                'full_name': obj.lead.full_name,
                'email': obj.lead.email,
                'phone': obj.lead.phone,
                'status': obj.lead.status
            }
        return None


class LeadLogCreateSerializer(BaseSerializer):
    """Simple serializer for creating lead logs"""

    class Meta:
        model = LeadLog
        fields = ['lead', 'action', 'description', 'notes', 'old_value', 'new_value']

    def create(self, validated_data):
        # Set the performed_by from the request user, handle anonymous users
        user = self.context['request'].user
        validated_data['performed_by'] = user if user.is_authenticated else None
        return super().create(validated_data)