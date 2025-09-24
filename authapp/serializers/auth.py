from django.contrib.auth import get_user_model
from rest_framework import  serializers

User = get_user_model()

class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        user = User(
            email=self.validated_data['email'],
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class LoginResponseSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()
    user_id = serializers.IntegerField()
    email = serializers.EmailField()
    groups = serializers.ListField(
        child=serializers.CharField()
    )

# For logout endpoint
class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()




# For refresh token endpoint
class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()