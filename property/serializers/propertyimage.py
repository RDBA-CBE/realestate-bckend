from rest_framework import serializers
from ..models import PropertyImage, Property


class PropertySimpleSerializer(serializers.ModelSerializer):
    """Simple serializer for property basic info"""
    class Meta:
        model = Property
        fields = ['id', 'title', 'city', 'state', 'status', 'listing_type']

class PropertyImageListSerializer(serializers.ModelSerializer):
    property_details = PropertySimpleSerializer(source='property', read_only=True)
    image_url = serializers.SerializerMethodField()
    file_size = serializers.SerializerMethodField()
    
    class Meta:
        model = PropertyImage
        fields = ['id', 'property', 'property_details', 'image', 'image_url', 'alt_text', 
                 'caption', 'is_primary', 'order', 'file_size', 'created_at']
    
    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None
    
    def get_file_size(self, obj):
        if obj.image:
            try:
                return obj.image.size
            except:
                return None
        return None


class PropertyImageDetailSerializer(serializers.ModelSerializer):
    property_details = PropertySimpleSerializer(source='property', read_only=True)
    image_url = serializers.SerializerMethodField()
    file_size = serializers.SerializerMethodField()
    image_dimensions = serializers.SerializerMethodField()
    
    class Meta:
        model = PropertyImage
        fields = '__all__'
        extra_fields = ['property_details', 'image_url', 'file_size', 'image_dimensions']
    
    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None
    
    def get_file_size(self, obj):
        if obj.image:
            try:
                return obj.image.size
            except:
                return None
        return None
    
    def get_image_dimensions(self, obj):
        if obj.image:
            try:
                return {
                    'width': obj.image.width,
                    'height': obj.image.height
                }
            except:
                return None
        return None


class PropertyImageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = ['property', 'image', 'alt_text', 'caption', 'is_primary', 'order']
    
    def validate(self, data):
        # Validate image file
        image = data.get('image')
        if image:
            # Check file size (limit to 10MB)
            if image.size > 10 * 1024 * 1024:
                raise serializers.ValidationError("Image file size cannot exceed 10MB")
            
            # Check file type
            allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp']
            if hasattr(image, 'content_type') and image.content_type not in allowed_types:
                raise serializers.ValidationError("Only JPEG, PNG, and WebP images are allowed")
        
        return data
    
    def create(self, validated_data):
        # Auto-set order if not provided
        if 'order' not in validated_data:
            property_instance = validated_data['property']
            last_order = PropertyImage.objects.filter(
                property=property_instance
            ).order_by('-order').first()
            validated_data['order'] = (last_order.order + 1) if last_order else 1
        
        return super().create(validated_data)


class PropertyImageUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = ['alt_text', 'caption', 'is_primary', 'order']
    
    def validate_order(self, value):
        if value < 0:
            raise serializers.ValidationError("Order cannot be negative")
        return value


class PropertyImageBulkUploadSerializer(serializers.Serializer):
    """Serializer for bulk image upload"""
    property = serializers.PrimaryKeyRelatedField(queryset=Property.objects.all())
    images = serializers.ListField(
        child=serializers.ImageField(),
        max_length=20,
        min_length=1
    )
    
    def validate_images(self, images):
        for image in images:
            # Check file size (limit to 10MB each)
            if image.size > 10 * 1024 * 1024:
                raise serializers.ValidationError(f"Image {image.name} exceeds 10MB limit")
            
            # Check file type
            allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp']
            if hasattr(image, 'content_type') and image.content_type not in allowed_types:
                raise serializers.ValidationError(f"Image {image.name} has invalid format")
        
        return images
    
    def create(self, validated_data):
        property_instance = validated_data['property']
        images = validated_data['images']
        
        # Get starting order
        last_order = PropertyImage.objects.filter(
            property=property_instance
        ).order_by('-order').first()
        start_order = (last_order.order + 1) if last_order else 1
        
        # Create image instances
        created_images = []
        for i, image in enumerate(images):
            property_image = PropertyImage.objects.create(
                property=property_instance,
                image=image,
                order=start_order + i,
                is_primary=(i == 0 and not PropertyImage.objects.filter(
                    property=property_instance, is_primary=True
                ).exists())
            )
            created_images.append(property_image)
        
        return created_images
