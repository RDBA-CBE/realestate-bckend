from rest_framework import serializers
from ..models import FloorPlan, Property


class PropertySimpleSerializer(serializers.ModelSerializer):
    """Simple serializer for property basic info"""
    class Meta:
        model = Property
        fields = ['id', 'title', 'city', 'state', 'status', 'price', 'listing_type']


class FloorPlanListSerializer(serializers.ModelSerializer):
    property_details = PropertySimpleSerializer(source='property', read_only=True)
    image_url = serializers.SerializerMethodField()
    file_size = serializers.SerializerMethodField()

    class Meta:
        model = FloorPlan
        fields = ['id', 'property', 'property_details', 'category', 'square_feet',
                 'price', 'image', 'image_url', 'file_size', 'created_at']

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


class FloorPlanDetailSerializer(serializers.ModelSerializer):
    property_details = PropertySimpleSerializer(source='property', read_only=True)
    image_url = serializers.SerializerMethodField()
    file_size = serializers.SerializerMethodField()
    image_dimensions = serializers.SerializerMethodField()

    class Meta:
        model = FloorPlan
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


class FloorPlanCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FloorPlan
        fields = ['property', 'category', 'square_feet', 'price', 'image']

    def validate(self, data):
        # Validate image file if provided
        image = data.get('image')
        if image:
            # Check file size (limit to 10MB)
            if image.size > 10 * 1024 * 1024:
                raise serializers.ValidationError("Image file size cannot exceed 10MB")

            # Check file type
            allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp', 'image/svg+xml']
            if hasattr(image, 'content_type') and image.content_type not in allowed_types:
                raise serializers.ValidationError("Only JPEG, PNG, WebP, and SVG images are allowed")

        # Validate square feet
        if data.get('square_feet') and data['square_feet'] <= 0:
            raise serializers.ValidationError("Square feet must be greater than 0")

        # Validate price
        if data.get('price') and data['price'] < 0:
            raise serializers.ValidationError("Price cannot be negative")

        return data


class FloorPlanUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FloorPlan
        fields = ['category', 'square_feet', 'price', 'image']

    def validate_square_feet(self, value):
        if value <= 0:
            raise serializers.ValidationError("Square feet must be greater than 0")
        return value

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Price cannot be negative")
        return value

    def validate(self, data):
        # Validate image file if provided
        image = data.get('image')
        if image:
            # Check file size (limit to 10MB)
            if image.size > 10 * 1024 * 1024:
                raise serializers.ValidationError("Image file size cannot exceed 10MB")

            # Check file type
            allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp', 'image/svg+xml']
            if hasattr(image, 'content_type') and image.content_type not in allowed_types:
                raise serializers.ValidationError("Only JPEG, PNG, WebP, and SVG images are allowed")

        return data


class FloorPlanBulkCreateSerializer(serializers.Serializer):
    """Serializer for bulk creating floor plans"""
    floor_plans = FloorPlanCreateSerializer(many=True)

    def create(self, validated_data):
        floor_plans_data = validated_data['floor_plans']
        floor_plans = []

        for floor_plan_data in floor_plans_data:
            floor_plan = FloorPlan.objects.create(**floor_plan_data)
            floor_plans.append(floor_plan)

        return floor_plans


class FloorPlanBulkUpdateSerializer(serializers.Serializer):
    """Serializer for bulk updating floor plans"""
    floor_plans = serializers.ListField(
        child=serializers.DictField(),
        allow_empty=False
    )

    def validate_floor_plans(self, value):
        """Validate that each floor plan has an id and valid update data"""
        for item in value:
            if 'id' not in item:
                raise serializers.ValidationError("Each floor plan must have an 'id' field")
            try:
                floor_plan = FloorPlan.objects.get(id=item['id'])
            except FloorPlan.DoesNotExist:
                raise serializers.ValidationError(f"Floor plan with id {item['id']} does not exist")

            # Validate update fields
            update_serializer = FloorPlanUpdateSerializer(data=item)
            if not update_serializer.is_valid():
                raise serializers.ValidationError(f"Invalid data for floor plan {item['id']}: {update_serializer.errors}")

        return value

    def update(self, instance, validated_data):
        floor_plans_data = validated_data['floor_plans']
        updated_floor_plans = []

        for floor_plan_data in floor_plans_data:
            floor_plan_id = floor_plan_data.pop('id')
            floor_plan = FloorPlan.objects.get(id=floor_plan_id)

            update_serializer = FloorPlanUpdateSerializer(floor_plan, data=floor_plan_data, partial=True)
            if update_serializer.is_valid():
                updated_floor_plan = update_serializer.save()
                updated_floor_plans.append(updated_floor_plan)

        return updated_floor_plans