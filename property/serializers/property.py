from rest_framework import serializers
from ..models import Property, PropertyImage, Project, PropertyType, Amenity
from django.contrib.auth import get_user_model

CustomUser = get_user_model()


class ProjectSerializer(serializers.ModelSerializer):
    developer_name = serializers.CharField(source='developer.get_full_name', read_only=True)
    developer_email = serializers.CharField(source='developer.email', read_only=True)
    total_properties = serializers.SerializerMethodField()
    
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'location', 'developer', 'developer_name', 
                 'developer_email', 'start_date', 'end_date', 'status', 'total_properties']
    
    def get_total_properties(self, obj):
        return obj.properties.count()


class PropertyTypeSerializer(serializers.ModelSerializer):
    properties_count = serializers.SerializerMethodField()
    
    class Meta:
        model = PropertyType
        fields = ['id', 'name', 'description', 'properties_count']
    
    def get_properties_count(self, obj):
        return obj.properties.count()


class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = ['id', 'name', 'description']


class PropertyImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = PropertyImage
        fields = ['id', 'image', 'image_url', 'alt_text', 'caption', 'is_primary', 'order']
    
    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None


class UserSimpleSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    user_type = serializers.CharField(read_only=True)
    
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name', 'full_name', 'user_type', 'phone']


class PropertyListSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source='project.name', read_only=True)
    property_type_name = serializers.CharField(source='property_type.name', read_only=True)
    owner_name = serializers.CharField(source='owner.get_full_name', read_only=True)
    agent_name = serializers.CharField(source='agent.get_full_name', read_only=True)
    primary_image = serializers.SerializerMethodField()
    amenities_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Property
        fields = ['id', 'title', 'city', 'state', 'status', 'price', 'price_per_sqft', 
                 'bedrooms', 'bathrooms', 'total_area', 'listing_type', 'furnishing',
                 'project_name', 'property_type_name', 'owner_name', 'agent_name', 
                 'primary_image', 'amenities_count', 'is_featured', 'views_count', 'created_at']
    
    def get_primary_image(self, obj):
        primary_image = obj.images.filter(is_primary=True).first()
        if primary_image:
            return PropertyImageSerializer(primary_image, context=self.context).data
        return None
    
    def get_amenities_count(self, obj):
        return obj.amenities.count()


class PropertyDetailSerializer(serializers.ModelSerializer):
    # Foreign key details
    project_details = ProjectSerializer(source='project', read_only=True)
    property_type_details = PropertyTypeSerializer(source='property_type', read_only=True)
    owner_details = UserSimpleSerializer(source='owner', read_only=True)
    agent_details = UserSimpleSerializer(source='agent', read_only=True)
    
    # Related data
    images = PropertyImageSerializer(many=True, read_only=True)
    amenities_details = AmenitySerializer(source='amenities', many=True, read_only=True)
    
    # Computed fields
    full_address = serializers.CharField(read_only=True)
    is_available = serializers.BooleanField(read_only=True)
    average_rating = serializers.DecimalField(max_digits=3, decimal_places=2, read_only=True)
    total_reviews = serializers.IntegerField(read_only=True)
    
    # Additional stats
    total_images = serializers.SerializerMethodField()
    primary_image = serializers.SerializerMethodField()
    
    class Meta:
        model = Property
        fields = '__all__'
        extra_fields = [
            'project_details', 'property_type_details', 'owner_details', 'agent_details',
            'images', 'amenities_details', 'full_address', 'is_available', 
            'average_rating', 'total_reviews', 'total_images', 'primary_image'
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
            return PropertyImageSerializer(primary_image, context=self.context).data
        return None


class PropertyCreateSerializer(serializers.ModelSerializer):
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


class PropertyUpdateSerializer(serializers.ModelSerializer):
    amenities = serializers.PrimaryKeyRelatedField(
        queryset=Amenity.objects.all(),
        many=True,
        required=False
    )
    
    class Meta:
        model = Property
        fields = [
            'title', 'description', 'status', 'price', 'address', 'city', 'state', 
            'country', 'postal_code', 'bedrooms', 'bathrooms', 'total_area', 
            'carpet_area', 'built_year', 'floor_number', 'total_floors',
            'maintenance_charges', 'security_deposit', 'furnishing', 'parking', 
            'parking_spaces', 'amenities', 'available_from', 'is_featured'
        ]
    
    def update(self, instance, validated_data):
        amenities = validated_data.pop('amenities', None)
        
        # Update regular fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        
        # Update amenities if provided
        if amenities is not None:
            instance.amenities.set(amenities)
        
        return instance


class PropertyImageUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = ['image', 'alt_text', 'caption', 'is_primary', 'order']
    
    def create(self, validated_data):
        property_instance = self.context['property']
        validated_data['property'] = property_instance
        return super().create(validated_data)