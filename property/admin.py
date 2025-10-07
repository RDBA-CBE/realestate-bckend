from django.contrib import admin
from .models import (
    Property, Project, ProjectPhase, ProjectDocument, PropertyType, Amenity,
    PropertyImage, PropertyVideo, VirtualTour
)

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
    list_display = ['name', 'category', 'is_active', 'created_at']
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['category', 'name']

@admin.register(PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):
    list_display = ['property', 'alt_text', 'is_primary', 'order', 'created_at']
    list_filter = ['is_primary', 'property']
    search_fields = ['property__title', 'alt_text', 'caption']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['property', 'order']

@admin.register(PropertyVideo)
class PropertyVideoAdmin(admin.ModelAdmin):
    list_display = ['property', 'title', 'duration', 'order', 'created_at']
    list_filter = ['property']
    search_fields = ['property__title', 'title', 'description']
    readonly_fields = ['created_at', 'updated_at', 'file_size']
    ordering = ['property', 'order']

@admin.register(VirtualTour)
class VirtualTourAdmin(admin.ModelAdmin):
    list_display = ['property', 'tour_type', 'provider', 'is_active', 'order', 'created_at']
    list_filter = ['tour_type', 'provider', 'is_active', 'property']
    search_fields = ['property__title', 'description', 'provider']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['property', 'order']
