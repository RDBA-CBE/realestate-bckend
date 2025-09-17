from django.contrib.auth import get_user_model
from rest_framework import  serializers

User = get_user_model()

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

class LoginResponseSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField()
    user_id = serializers.IntegerField()
    email = serializers.EmailField()
    groups = serializers.ListField(
        child=serializers.CharField()
    )

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()