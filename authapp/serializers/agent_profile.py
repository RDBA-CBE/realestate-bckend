from rest_framework import serializers
from ..models.agentprofile import AgentProfile

class AgentProfileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgentProfile
        fields = ['id', 'user', 'agency_name']

class AgentProfileDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgentProfile
        fields = '__all__'

class AgentProfileCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgentProfile
        fields = ['user', 'agency_name']

class AgentProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgentProfile
        fields = ['agency_name']
