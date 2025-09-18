from rest_framework import viewsets, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from authapp.serializers.auth import RegistrationSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class RegistrationViewSet(viewsets.ModelViewSet):
    """
    User Registration ViewSet
    """
    serializer_class = RegistrationSerializer
    queryset = User.objects.all()
    http_method_names = ['post']

    @extend_schema(
        request=RegistrationSerializer,
        responses={201: {"success": "User created successfully"}},
        summary="Register a new user",
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"success": "User created successfully"}, status=status.HTTP_201_CREATED)