from rest_framework import serializers
from ..models.property import ProjectDocument

class ProjectDocumentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectDocument
        fields = ['id', 'project', 'name', 'uploaded_at']

class ProjectDocumentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectDocument
        fields = '__all__'

class ProjectDocumentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectDocument
        fields = ['project', 'file', 'name']

class ProjectDocumentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectDocument
        fields = ['file', 'name']
