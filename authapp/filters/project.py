import django_filters
from authapp.models.property import Project

class ProjectFilter(django_filters.FilterSet):
    class Meta:
        model = Project
        fields = ['name', 'location', 'developer', 'status']
