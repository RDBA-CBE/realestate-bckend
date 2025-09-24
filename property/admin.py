from django.contrib import admin
from .models import Property, Project, ProjectPhase, ProjectDocument, PropertyType, Amenity

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ['title', 'city', 'status', 'price', 'listing_type', 'created_at']
    list_filter = ['status', 'listing_type', 'property_type', 'city', 'state']
    search_fields = ['title', 'city', 'address']
    readonly_fields = ['created_at', 'updated_at', 'price_per_sqft', 'views_count']

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'developer', 'status', 'start_date', 'end_date']
    list_filter = ['status', 'developer']
    search_fields = ['name', 'location']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(ProjectPhase)
class ProjectPhaseAdmin(admin.ModelAdmin):
    list_display = ['name', 'project', 'start_date', 'end_date']
    list_filter = ['project']
    search_fields = ['name', 'project__name']

@admin.register(ProjectDocument)
class ProjectDocumentAdmin(admin.ModelAdmin):
    list_display = ['name', 'project', 'uploaded_at']
    list_filter = ['project', 'uploaded_at']
    search_fields = ['name', 'project__name']
    readonly_fields = ['uploaded_at']

@admin.register(PropertyType)
class PropertyTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']

@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description']
    list_filter = ['name']
    readonly_fields = ['created_at', 'updated_at']
