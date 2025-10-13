from rest_framework import serializers
from django.utils import timezone
from common.serializers import BaseSerializer
from ..models import ProjectPhase, Project


class ProjectSimpleSerializer(serializers.ModelSerializer):
    """Simple project serializer for phase references"""
    developer_name = serializers.CharField(source='developer.company_name', read_only=True)
    total_phases = serializers.SerializerMethodField()
    
    class Meta:
        model = Project
        fields = ['id', 'name', 'developer_name', 'total_phases', 'status']
    
    def get_total_phases(self, obj):
        return obj.phases.count()


class ProjectPhaseListSerializer(BaseSerializer):
    project_details = ProjectSimpleSerializer(source='project', read_only=True)
    duration_days = serializers.SerializerMethodField()
    status_display = serializers.SerializerMethodField()
    progress_percentage = serializers.SerializerMethodField()
    
    class Meta:
        model = ProjectPhase
        fields = ['id', 'name', 'start_date', 'end_date', 'duration_days', 
                 'status_display', 'progress_percentage', 'project_details']
    
    def get_duration_days(self, obj):
        if obj.start_date and obj.end_date:
            return (obj.end_date - obj.start_date).days
        return None
    
    def get_status_display(self, obj):
        now = timezone.now().date()
        if obj.start_date and obj.end_date:
            if now < obj.start_date:
                return "Not Started"
            elif now > obj.end_date:
                return "Completed"
            else:
                return "In Progress"
        return "Unknown"
    
    def get_progress_percentage(self, obj):
        now = timezone.now().date()
        if obj.start_date and obj.end_date:
            if now < obj.start_date:
                return 0
            elif now > obj.end_date:
                return 100
            else:
                total_days = (obj.end_date - obj.start_date).days
                elapsed_days = (now - obj.start_date).days
                return round((elapsed_days / total_days) * 100, 1) if total_days > 0 else 0
        return 0


class ProjectPhaseDetailSerializer(BaseSerializer):
    project_details = ProjectSimpleSerializer(source='project', read_only=True)
    duration_days = serializers.SerializerMethodField()
    status_display = serializers.SerializerMethodField()
    progress_percentage = serializers.SerializerMethodField()
    time_remaining = serializers.SerializerMethodField()
    is_overdue = serializers.SerializerMethodField()
    
    class Meta:
        model = ProjectPhase
        fields = '__all__'
        extra_fields = ['project_details', 'duration_days', 'status_display', 
                       'progress_percentage', 'time_remaining', 'is_overdue']
    
    def get_duration_days(self, obj):
        if obj.start_date and obj.end_date:
            return (obj.end_date - obj.start_date).days
        return None
    
    def get_status_display(self, obj):
        now = timezone.now().date()
        if obj.start_date and obj.end_date:
            if now < obj.start_date:
                return "Not Started"
            elif now > obj.end_date:
                return "Completed"
            else:
                return "In Progress"
        return "Unknown"
    
    def get_progress_percentage(self, obj):
        now = timezone.now().date()
        if obj.start_date and obj.end_date:
            if now < obj.start_date:
                return 0
            elif now > obj.end_date:
                return 100
            else:
                total_days = (obj.end_date - obj.start_date).days
                elapsed_days = (now - obj.start_date).days
                return round((elapsed_days / total_days) * 100, 1) if total_days > 0 else 0
        return 0
    
    def get_time_remaining(self, obj):
        now = timezone.now().date()
        if obj.end_date:
            remaining_days = (obj.end_date - now).days
            if remaining_days > 0:
                return f"{remaining_days} days"
            elif remaining_days == 0:
                return "Today"
            else:
                return f"Overdue by {abs(remaining_days)} days"
        return "Unknown"
    
    def get_is_overdue(self, obj):
        now = timezone.now().date()
        if obj.end_date:
            return now > obj.end_date
        return False


class ProjectPhaseCreateSerializer(BaseSerializer):
    class Meta:
        model = ProjectPhase
        fields = ['project', 'name', 'description', 'start_date', 'end_date']
    
    def validate(self, data):
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        
        if start_date and end_date:
            if start_date >= end_date:
                raise serializers.ValidationError(
                    "Start date must be before end date"
                )
            
            # Check for overlapping phases in the same project
            project = data.get('project')
            if project:
                overlapping_phases = ProjectPhase.objects.filter(
                    project=project,
                    start_date__lt=end_date,
                    end_date__gt=start_date
                )
                if overlapping_phases.exists():
                    raise serializers.ValidationError(
                        "This phase overlaps with existing phases in the project"
                    )
        
        return data


class ProjectPhaseUpdateSerializer(BaseSerializer):
    class Meta:
        model = ProjectPhase
        fields = ['name', 'description', 'start_date', 'end_date']
    
    def validate(self, data):
        start_date = data.get('start_date', self.instance.start_date)
        end_date = data.get('end_date', self.instance.end_date)
        
        if start_date and end_date:
            if start_date >= end_date:
                raise serializers.ValidationError(
                    "Start date must be before end date"
                )
            
            # Check for overlapping phases in the same project (excluding current instance)
            overlapping_phases = ProjectPhase.objects.filter(
                project=self.instance.project,
                start_date__lt=end_date,
                end_date__gt=start_date
            ).exclude(pk=self.instance.pk)
            
            if overlapping_phases.exists():
                raise serializers.ValidationError(
                    "This phase overlaps with existing phases in the project"
                )
        
        return data


class ProjectPhaseStatsSerializer(BaseSerializer):
    """Serializer for project phase statistics"""
    total_duration = serializers.SerializerMethodField()
    completion_percentage = serializers.SerializerMethodField()
    days_since_start = serializers.SerializerMethodField()
    is_critical_path = serializers.SerializerMethodField()
    
    class Meta:
        model = ProjectPhase
        fields = ['id', 'name', 'start_date', 'end_date', 'total_duration', 
                 'completion_percentage', 'days_since_start', 'is_critical_path']
    
    def get_total_duration(self, obj):
        if obj.start_date and obj.end_date:
            return (obj.end_date - obj.start_date).days
        return 0
    
    def get_completion_percentage(self, obj):
        now = timezone.now().date()
        if obj.start_date and obj.end_date:
            if now < obj.start_date:
                return 0
            elif now > obj.end_date:
                return 100
            else:
                total_days = (obj.end_date - obj.start_date).days
                elapsed_days = (now - obj.start_date).days
                return round((elapsed_days / total_days) * 100, 1) if total_days > 0 else 0
        return 0
    
    def get_days_since_start(self, obj):
        if obj.start_date:
            return (timezone.now().date() - obj.start_date).days
        return 0
    
    def get_is_critical_path(self, obj):
        # Simple heuristic: phases with no buffer time are critical
        project_phases = obj.project.phases.all().order_by('start_date')
        phase_list = list(project_phases)
        
        try:
            current_index = phase_list.index(obj)
            if current_index < len(phase_list) - 1:
                next_phase = phase_list[current_index + 1]
                if obj.end_date and next_phase.start_date:
                    buffer_days = (next_phase.start_date - obj.end_date).days
                    return buffer_days <= 0
        except (ValueError, IndexError):
            pass
        
        return False
