from rest_framework import serializers
from common.serializers import BaseSerializer
from ..models import ProjectDocument, Project


class ProjectSimpleSerializer(serializers.ModelSerializer):
    """Simple project serializer for document references"""
    developer_name = serializers.CharField(source='developer.company_name', read_only=True)
    total_properties = serializers.SerializerMethodField()
    
    class Meta:
        model = Project
        fields = ['id', 'name', 'developer_name', 'total_properties', 'status']
    
    def get_total_properties(self, obj):
        return obj.properties.count()


class ProjectDocumentListSerializer(BaseSerializer):
    project_details = ProjectSimpleSerializer(source='project', read_only=True)
    file_size = serializers.SerializerMethodField()
    file_type = serializers.SerializerMethodField()
    
    class Meta:
        model = ProjectDocument
        fields = ['id', 'name', 'file_size', 'file_type', 'uploaded_at', 'project_details']
    
    def get_file_size(self, obj):
        try:
            if obj.file and hasattr(obj.file, 'size'):
                size = obj.file.size
                if size < 1024:
                    return f"{size} B"
                elif size < 1024 * 1024:
                    return f"{size / 1024:.1f} KB"
                else:
                    return f"{size / (1024 * 1024):.1f} MB"
        except:
            pass
        return "Unknown"
    
    def get_file_type(self, obj):
        if obj.file and hasattr(obj.file, 'name'):
            return obj.file.name.split('.')[-1].upper() if '.' in obj.file.name else 'Unknown'
        return "Unknown"


class ProjectDocumentDetailSerializer(BaseSerializer):
    project_details = ProjectSimpleSerializer(source='project', read_only=True)
    file_size = serializers.SerializerMethodField()
    file_type = serializers.SerializerMethodField()
    download_url = serializers.SerializerMethodField()
    
    class Meta:
        model = ProjectDocument
        fields = '__all__'
        extra_fields = ['project_details', 'file_size', 'file_type', 'download_url']
    
    def get_file_size(self, obj):
        try:
            if obj.file and hasattr(obj.file, 'size'):
                size = obj.file.size
                if size < 1024:
                    return f"{size} B"
                elif size < 1024 * 1024:
                    return f"{size / 1024:.1f} KB"
                else:
                    return f"{size / (1024 * 1024):.1f} MB"
        except:
            pass
        return "Unknown"
    
    def get_file_type(self, obj):
        if obj.file and hasattr(obj.file, 'name'):
            return obj.file.name.split('.')[-1].upper() if '.' in obj.file.name else 'Unknown'
        return "Unknown"
    
    def get_download_url(self, obj):
        if obj.file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.file.url)
            return obj.file.url
        return None


class ProjectDocumentCreateSerializer(BaseSerializer):
    class Meta:
        model = ProjectDocument
        fields = ['project', 'file', 'name']
    
    def validate_file(self, value):
        # Check file size (limit to 10MB)
        if value.size > 10 * 1024 * 1024:
            raise serializers.ValidationError("File size must be less than 10MB")
        
        # Check file type
        allowed_types = ['pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png', 'txt']
        file_extension = value.name.split('.')[-1].lower() if '.' in value.name else ''
        if file_extension not in allowed_types:
            raise serializers.ValidationError(
                f"File type '{file_extension}' not allowed. Allowed types: {', '.join(allowed_types)}"
            )
        
        return value


class ProjectDocumentUpdateSerializer(BaseSerializer):
    class Meta:
        model = ProjectDocument
        fields = ['file', 'name']
    
    def validate_file(self, value):
        if value:
            # Check file size (limit to 10MB)
            if value.size > 10 * 1024 * 1024:
                raise serializers.ValidationError("File size must be less than 10MB")
            
            # Check file type
            allowed_types = ['pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png', 'txt']
            file_extension = value.name.split('.')[-1].lower() if '.' in value.name else ''
            if file_extension not in allowed_types:
                raise serializers.ValidationError(
                    f"File type '{file_extension}' not allowed. Allowed types: {', '.join(allowed_types)}"
                )
        
        return value
