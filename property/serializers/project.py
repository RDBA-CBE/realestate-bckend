from rest_framework import serializers
from property.models import Project
from authapp.models import CustomUser

class DeveloperSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name']

class ProjectListSerializer(serializers.ModelSerializer):
    developer = DeveloperSerializer(read_only=True)
    class Meta:
        model = Project
        fields = ['id', 'name', 'location', 'status', 'developer']

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
        fields = ['name','description', 'location', 'start_date', 'end_date', 'status']