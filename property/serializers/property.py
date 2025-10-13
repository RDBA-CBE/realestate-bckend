from rest_framework import serializers
from ..models import Property
from .propertyimage import PropertyImageListSerializer
from .propertyvideo import PropertyVideoListSerializer
from .virtualtour import VirtualTourListSerializer
from .project import ProjectListSerializer
from .propertytype import PropertyTypeListSerializer
from .amenity import AmenityListSerializer
from authapp.serializers.customuser import CustomUserListSerializer

class PropertyListSerializer(serializers.ModelSerializer):
    primary_image = serializers.SerializerMethodField()
    images_count = serializers.SerializerMethodField() 
    videos_count = serializers.SerializerMethodField()
    virtual_tours_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Property
        fields = [
            'id', 'title', 'city', 'state', 'status', 'price', 'listing_type',
            'property_type', 'project', 'agent', 'developers', 'amenities',
            'bedrooms', 'bathrooms', 'total_area', 'monthly_rent',
            'primary_image', 'images_count', 'videos_count', 'virtual_tours_count'
        ]
    
    def get_primary_image(self, obj):
        primary_image = obj.images.filter(is_primary=True).first()
        if primary_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(primary_image.image.url)
            return primary_image.image.url
        return None
    
    def get_images_count(self, obj):
        return obj.images.count()
    
    def get_videos_count(self, obj):
        return obj.videos.count()
    
    def get_virtual_tours_count(self, obj):
        return obj.virtual_tours.filter(is_active=True).count()

class PropertyDetailSerializer(serializers.ModelSerializer):
    images = PropertyImageListSerializer(many=True, read_only=True)
    videos = PropertyVideoListSerializer(many=True, read_only=True)
    virtual_tours = VirtualTourListSerializer(many=True, read_only=True)
    project = ProjectListSerializer(read_only=True)
    property_type = PropertyTypeListSerializer(read_only=True)
    agent = CustomUserListSerializer(read_only=True)
    developers = CustomUserListSerializer(many=True, read_only=True)
    amenities = AmenityListSerializer(many=True, read_only=True)
    
    class Meta:
        model = Property
        fields = '__all__'

class PropertyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'

class PropertyUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = [
            'title', 'description', 'status', 'price', 'address', 'city', 'state', 'country', 
            'postal_code', 'bedrooms', 'bathrooms', 'total_area', 'carpet_area',
            'plot_area', 'land_type_zone', 'built_up_area', 'balconies', 
            'facing_direction', 'monthly_rent', 'rent_duration', 
            'lease_total_amount', 'lease_duration', 'furnishing', 'parking',
            'parking_spaces', 'available_from', 'is_featured', 'project',
            'property_type', 'agent', 'developers', 'amenities'
        ]