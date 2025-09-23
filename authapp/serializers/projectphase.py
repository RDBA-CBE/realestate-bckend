from rest_framework import serializers
from ..models.property import ProjectPhase

class ProjectPhaseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectPhase
        fields = ['id', 'project', 'name', 'start_date', 'end_date']

class ProjectPhaseDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectPhase
        fields = '__all__'

class ProjectPhaseCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectPhase
        fields = ['project', 'name', 'description', 'start_date', 'end_date']

class ProjectPhaseUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectPhase
        fields = ['name', 'description', 'start_date', 'end_date']
