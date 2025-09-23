from rest_framework import serializers
from ..models.property import Project, ProjectPhase, ProjectDocument

class ProjectListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'location', 'status']

class ProjectDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

class ProjectCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['name', 'description', 'location', 'developer', 'start_date', 'end_date', 'status']

class ProjectUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['description', 'location', 'start_date', 'end_date', 'status']


