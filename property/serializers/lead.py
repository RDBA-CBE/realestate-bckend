from rest_framework import serializers
from ..models import Lead
from common.serializers import BaseSerializer
from .property import PropertyListSerializer
from authapp.serializers.customuser import CustomUserListSerializer

class LeadListSerializer(BaseSerializer):
    property_details = PropertyListSerializer(source='interested_property', read_only=True)
    assigned_to_details = CustomUserListSerializer(source='assigned_to', read_only=True)
    assigned_by_details = CustomUserListSerializer(source='assigned_by', read_only=True)
    full_name = serializers.SerializerMethodField()
    days_since_last_contact = serializers.SerializerMethodField()
    days_until_next_follow_up = serializers.SerializerMethodField()

    class Meta:
        model = Lead
        fields = [
            'id', 'first_name', 'last_name', 'full_name', 'email', 'phone', 'alternate_phone',
            'property_details', 'interested_property', 'status', 'priority', 'lead_source', 'lead_source_details',
            'assigned_to', 'assigned_to_details', 'next_follow_up',
            'days_since_last_contact', 'days_until_next_follow_up',
            'budget_min', 'budget_max', 'preferred_location', 'requirements',
            'created_at','created_by', 'company_name', 'occupation', 'address', 'city', 'state', 'country', 'postal_code',
            'newsletter_subscribed', 'sms_marketing','assigned_by_details'
        ]

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    def get_days_since_last_contact(self, obj):
        return obj.days_since_last_contact

    def get_days_until_next_follow_up(self, obj):
        return obj.days_until_next_follow_up

class LeadDetailSerializer(BaseSerializer):
    property_details = PropertyListSerializer(source='interested_property', read_only=True)
    assigned_to_details = CustomUserListSerializer(source='assigned_to', read_only=True)
    assigned_by_details = CustomUserListSerializer(source='assigned_by', read_only=True)
    full_name = serializers.SerializerMethodField()
    days_since_last_contact = serializers.SerializerMethodField()
    days_until_next_follow_up = serializers.SerializerMethodField()

    class Meta:
        model = Lead
        fields = [
            'id', 'first_name', 'last_name', 'full_name', 'email', 'phone', 'alternate_phone',
            'property_details', 'interested_property', 'status', 'priority', 'lead_source', 'lead_source_details',
            'assigned_to', 'assigned_to_details', 'assigned_by', 'assigned_by_details', 'assigned_at',
            'next_follow_up', 'last_contacted', 'contact_count',
            'days_since_last_contact', 'days_until_next_follow_up',
            'budget_min', 'budget_max', 'preferred_location', 'requirements',
            'created_at', 'created_by', 'company_name', 'occupation', 'address', 'city', 'state', 'country', 'postal_code',
            'newsletter_subscribed', 'sms_marketing'
        ]

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    def get_days_since_last_contact(self, obj):
        return obj.days_since_last_contact

    def get_days_until_next_follow_up(self, obj):
        return obj.days_until_next_follow_up

class LeadCreateSerializer(BaseSerializer):
    class Meta:
        model = Lead
        fields = [
            'first_name', 'last_name', 'email', 'phone', 'alternate_phone',
            'interested_property', 'budget_min', 'budget_max', 'preferred_location',
            'requirements', 'status', 'priority', 'lead_source', 'lead_source_details',
            'assigned_to', 'next_follow_up', 'company_name', 'occupation',
            'address', 'city', 'state', 'country', 'postal_code',
            'newsletter_subscribed', 'sms_marketing'
        ]
        read_only_fields = ['assigned_by', 'assigned_at', 'last_contacted', 'contact_count']

    def validate_email(self, value):
        if Lead.objects.filter(email=value, interested_property=self.initial_data.get('interested_property')).exists():
            raise serializers.ValidationError("A lead with this email already exists for this property")
        return value

    def validate_phone(self, value):
        if Lead.objects.filter(phone=value, interested_property=self.initial_data.get('interested_property')).exists():
            raise serializers.ValidationError("A lead with this phone number already exists for this property")
        return value

    def validate(self, data):
        budget_min = data.get('budget_min')
        budget_max = data.get('budget_max')
        if budget_min and budget_max and budget_min > budget_max:
            raise serializers.ValidationError("Minimum budget cannot be greater than maximum budget")
        return data

    def create(self, validated_data):
        # Handle assigned_by field
        if 'assigned_by' not in validated_data:
            request = self.context.get('request')
            if request and request.user.is_authenticated:
                validated_data['assigned_by'] = request.user
        
        # Set assigned_at timestamp if assigned_to is provided
        if validated_data.get('assigned_to') and 'assigned_at' not in validated_data:
            from django.utils import timezone
            validated_data['assigned_at'] = timezone.now()
        
        return super().create(validated_data)

class LeadUpdateSerializer(BaseSerializer):
    class Meta:
        model = Lead
        fields = [
            'first_name', 'last_name', 'email', 'phone', 'alternate_phone',
            'budget_min', 'budget_max', 'preferred_location', 'requirements',
            'status', 'priority', 'lead_source', 'lead_source_details',
            'assigned_to', 'next_follow_up', 'company_name', 'occupation',
            'address', 'city', 'state', 'country', 'postal_code',
            'newsletter_subscribed', 'sms_marketing'
        ]
        read_only_fields = ['interested_property', 'assigned_by', 'assigned_at', 'last_contacted', 'contact_count']

    def validate_email(self, value):
        if Lead.objects.filter(email=value, interested_property=self.instance.interested_property).exclude(pk=self.instance.pk).exists():
            raise serializers.ValidationError("A lead with this email already exists for this property")
        return value

    def validate_phone(self, value):
        if Lead.objects.filter(phone=value, interested_property=self.instance.interested_property).exclude(pk=self.instance.pk).exists():
            raise serializers.ValidationError("A lead with this phone number already exists for this property")
        return value

    def validate(self, data):
        budget_min = data.get('budget_min')
        budget_max = data.get('budget_max')
        if budget_min and budget_max and budget_min > budget_max:
            raise serializers.ValidationError("Minimum budget cannot be greater than maximum budget")
        return data

    def update(self, instance, validated_data):
        if 'assigned_to' in validated_data and validated_data['assigned_to'] != instance.assigned_to:
            from django.utils import timezone
            validated_data['assigned_at'] = timezone.now()
        return super().update(instance, validated_data)
