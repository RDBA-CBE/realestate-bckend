from rest_framework import serializers
from common.serializers import BaseSerializer
from ..models import Property, Amenity
from .propertyimage import PropertyImageListSerializer
from .propertyvideo import PropertyVideoListSerializer
from .virtualtour import VirtualTourListSerializer
from .project import ProjectListSerializer
from .propertytype import PropertyTypeListSerializer
from .amenity import AmenityListSerializer
from authapp.serializers.customuser import CustomUserListSerializer

class PropertyListSerializer(BaseSerializer):
    primary_image = serializers.SerializerMethodField()
    images_count = serializers.SerializerMethodField() 
    images = PropertyImageListSerializer(many=True, read_only=True)
    project = ProjectListSerializer(read_only=True)
    videos_count = serializers.SerializerMethodField()
    virtual_tours_count = serializers.SerializerMethodField()
    developer = CustomUserListSerializer(read_only=True)
    property_type = PropertyTypeListSerializer(read_only=True)
    agent = CustomUserListSerializer(read_only=True)


    class Meta:
        model = Property
        fields = '__all__'
    
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

class PropertyDetailSerializer(BaseSerializer):
    images = PropertyImageListSerializer(many=True, read_only=True)
    videos = PropertyVideoListSerializer(many=True, read_only=True)
    virtual_tours = VirtualTourListSerializer(many=True, read_only=True)
    project = ProjectListSerializer(read_only=True)
    property_type = PropertyTypeListSerializer(read_only=True)
    agent = CustomUserListSerializer(read_only=True)
    developer = CustomUserListSerializer(read_only=True)
    amenities = AmenityListSerializer(many=True, read_only=True)
    
    class Meta:
        model = Property
        fields = '__all__'
        extra_fields = [
            'project_details', 'property_type_details', 'owner_details', 'agent_details',
            'images', 'amenities_details', 'full_address', 'is_available', 
            'average_rating', 'total_reviews', 'total_images', 'primary_image',
        ]
    
    def get_fields(self):
        fields = super().get_fields()
        # Add extra fields to the serializer
        for field in self.Meta.extra_fields:
            if field not in fields and hasattr(self, f'get_{field}'):
                fields[field] = serializers.SerializerMethodField()
        return fields
    
    def get_total_images(self, obj):
        return obj.images.count()
    
    def get_primary_image(self, obj):
        primary_image = obj.images.filter(is_primary=True).first()
        if primary_image:
            return PropertyImageListSerializer(primary_image, context=self.context).data
        return None


class PropertyCreateSerializer(BaseSerializer):
    amenities = serializers.PrimaryKeyRelatedField(
        queryset=Amenity.objects.all(),
        many=True,
        required=False
    )
    
    class Meta:
        model = Property
        fields = '__all__'
        read_only_fields = ['slug', 'price_per_sqft', 'views_count', 'created_at', 'updated_at']
    
    def validate(self, data):
        # Custom validation
        if data.get('built_year') and data['built_year'] > 2030:
            raise serializers.ValidationError("Built year cannot be in the future beyond 2030")
        
        if data.get('bedrooms', 0) < 0:
            raise serializers.ValidationError("Bedrooms cannot be negative")
        
        if data.get('bathrooms', 0) < 0:
            raise serializers.ValidationError("Bathrooms cannot be negative")
        
        if data.get('total_area') and data['total_area'] <= 0:
            raise serializers.ValidationError("Total area must be greater than 0")
        
        return data
    
    def create(self, validated_data):
        amenities = validated_data.pop('amenities', [])
        property_instance = Property.objects.create(**validated_data)
        
        if amenities:
            property_instance.amenities.set(amenities)
        
        return property_instance


class PropertyUpdateSerializer(BaseSerializer):
    amenities = serializers.PrimaryKeyRelatedField(
        queryset=Amenity.objects.all(),
        many=True,
        required=False
    )
    
    class Meta:
        model = Property
        fields = [
            'title', 'description', 'status', 'price', 'address', 'city', 'state', 'country', 
            'postal_code', 'bedrooms', 'bathrooms', 'total_area', 'carpet_area',
            'plot_area', 'land_type_zone', 'built_up_area', 'balconies', 
            'facing_direction', 'monthly_rent', 'rent_duration', 
            'lease_total_amount', 'lease_duration', 'furnishing', 'parking',
            'parking_spaces', 'available_from', 'is_featured', 'project',
            'property_type', 'agent', 'developer', 'amenities','highlightes', 'rera_id'
        ]