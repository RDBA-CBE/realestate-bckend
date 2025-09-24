from django.contrib.auth import authenticate, get_user_model
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken
from authapp.serializers.auth import (
    LoginSerializer, LoginResponseSerializer, 
    LogoutSerializer, RefreshTokenSerializer
)

User = get_user_model()


class AuthViewSet(viewsets.ViewSet):
    
    @extend_schema(
        request=RefreshTokenSerializer,
        responses={"200": {"access": "New access token"}},
        summary="Refresh JWT access token",
        description="Pass a valid refresh token to get a new access token."
    )
    @action(detail=False, methods=["post"], url_path="refresh-token")
    def refresh_token(self, request):
        serializer = RefreshTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            refresh_token = serializer.validated_data["refresh"]
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
            return Response({"access": access_token}, status=status.HTTP_200_OK)
        except Exception:
            return Response({"error": "Invalid or expired refresh token"}, status=status.HTTP_400_BAD_REQUEST)
    """
    JWT Auth ViewSet (email as username, returns groups in response)
    """

    @extend_schema(
        request=LoginSerializer,
        responses=LoginResponseSerializer,
        summary="Login with email & password",
        description="Returns JWT tokens and user details with groups"
    )
    @action(detail=False, methods=["post"])
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        user = authenticate(request, username=email, password=password)
        if not user:
            return Response(
                {"error": "Invalid email or password"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        refresh = RefreshToken.for_user(user)
        groups = list(user.groups.values_list("id", "name"))
        groups_data = [{"id": g[0], "name": g[1]} for g in groups]

        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user_id": user.id,
            "email": user.email,
            "groups": groups_data,
            "name": user.get_full_name(),
            "first_name": user.first_name,
            "last_name": user.last_name,
            
        }, status=status.HTTP_200_OK)

    @extend_schema(
        request=LogoutSerializer,
        responses={"200": {"success": "Logged out successfully"}},
        summary="Logout by blacklisting refresh token",
        description="Pass a valid refresh token to logout"
    )
    @action(detail=False, methods=["post"])
    def logout(self, request):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            refresh_token = serializer.validated_data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"success": "Logged out successfully"}, status=status.HTTP_200_OK)
        except Exception:
            return Response({"error": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)
