from rest_framework import serializers
from property.models import Project, ProjectPhase, ProjectDocument
from authapp.models import CustomUser


class ProjectPhaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectPhase
        fields = ['id', 'name', 'description', 'start_date', 'end_date']


class ProjectDocumentSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()
    file_size = serializers.SerializerMethodField()
    
    class Meta:
        model = ProjectDocument
        fields = ['id', 'name', 'file', 'file_url', 'file_size', 'uploaded_at']
    
    def get_file_url(self, obj):
        if obj.file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.file.url)
            return obj.file.url
        return None
    
    def get_file_size(self, obj):
        if obj.file:
            return obj.file.size
        return None


class DeveloperSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    user_type = serializers.CharField(read_only=True)
    total_projects = serializers.SerializerMethodField()
    
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name', 'full_name', 'user_type', 
                 'phone', 'total_projects']
    
    def get_total_projects(self, obj):
        return obj.projects.count()


class ProjectListSerializer(serializers.ModelSerializer):
    developer = DeveloperSerializer(read_only=True)
    developer_name = serializers.CharField(source='developer.get_full_name', read_only=True)
    developer_email = serializers.CharField(source='developer.email', read_only=True)
    total_properties = serializers.SerializerMethodField()
    total_phases = serializers.SerializerMethodField()
    property_count = serializers.IntegerField(source='properties.count', read_only=True)
    
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'location', 'developer', 'developer_name', 
                 'developer_email', 'start_date', 'end_date', 'status', 'total_properties', 
                 'total_phases', 'created_at','property_count']
    
    def get_total_properties(self, obj):
        return obj.properties.count()
    
    def get_total_phases(self, obj):
        return obj.phases.count()


class ProjectDetailSerializer(serializers.ModelSerializer):
    developers_details = DeveloperSerializer(source='developers', many=True, read_only=True)
    phases = ProjectPhaseSerializer(many=True, read_only=True)
    documents = ProjectDocumentSerializer(many=True, read_only=True)
    
    # Property statistics
    total_properties = serializers.SerializerMethodField()
    available_properties = serializers.SerializerMethodField()
    sold_properties = serializers.SerializerMethodField()
    average_price = serializers.SerializerMethodField()
    
    class Meta:
        model = Project
        fields = '__all__'
        extra_fields = [
            'developers_details', 'phases', 'documents',
            'total_properties', 'available_properties', 'sold_properties', 'average_price'
        ]
    
    def get_total_properties(self, obj):
        return obj.properties.count()
    
    def get_available_properties(self, obj):
        return obj.properties.filter(status='available').count()
    
    def get_sold_properties(self, obj):
        return obj.properties.filter(status='sold').count()
    
    def get_average_price(self, obj):
        from django.db.models import Avg
        avg_price = obj.properties.aggregate(avg_price=Avg('price'))['avg_price']
        return avg_price if avg_price else 0


class ProjectCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['name', 'description', 'location', 'developers', 'start_date', 'end_date', 'status']
    
    def validate(self, data):
        if data.get('start_date') and data.get('end_date'):
            if data['start_date'] > data['end_date']:
                raise serializers.ValidationError("Start date cannot be after end date")
        return data


class ProjectUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['name', 'description', 'location', 'start_date', 'end_date', 'status']
    
    def validate(self, data):
        if data.get('start_date') and data.get('end_date'):
            if data['start_date'] > data['end_date']:
                raise serializers.ValidationError("Start date cannot be after end date")
        return data


class ProjectPhaseCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectPhase
        fields = ['name', 'description', 'start_date', 'end_date']
    
    def create(self, validated_data):
        project = self.context['project']
        validated_data['project'] = project
        return super().create(validated_data)


class ProjectDocumentUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectDocument
        fields = ['name', 'file']
    
    def create(self, validated_data):
        project = self.context['project']
        validated_data['project'] = project
        return super().create(validated_data)