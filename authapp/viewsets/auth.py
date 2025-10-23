from django.contrib.auth import authenticate, get_user_model
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from authapp.serializers.auth import (
    LoginSerializer, LoginResponseSerializer,
    LogoutSerializer, RefreshTokenSerializer,
)
from property.models import PropertyWishlist

User = get_user_model()


class AuthViewSet(viewsets.ViewSet):
    """
    JWT Authentication ViewSet:
    - Login (auto creates profile if missing)
    - Refresh access token
    - Logout (blacklist refresh)
    """

    @extend_schema(
        request=LoginSerializer,
        responses=LoginResponseSerializer,
        summary="Login with email & password (auto create profile)",
    )
    @action(detail=False, methods=["post"])
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        user = User.objects.filter(email=email).first()
        if not user:
            return Response({"error": "Invalid email or password"}, status=401)

        # Block unapproved users
        if getattr(user, "account_status", "approved") != "approved":
            messages = {
                "pending_review": "Your account is pending admin approval",
                "rejected": "Your account application was rejected",
                "unverified": "Your email address is not verified",
                "suspended": "Your account has been suspended",
            }
            return Response(
                {"error": messages.get(user.account_status, "Account not approved"),
                 "account_status": user.account_status},
                status=403,
            )

        # Authenticate
        user = authenticate(request, username=email, password=password)
        if not user:
            return Response({"error": "Invalid email or password"}, status=401)
        if not user.is_active:
            return Response({"error": "Account is inactive"}, status=403)

        # Generate tokens
        refresh = RefreshToken.for_user(user)
        groups = list(user.groups.values("id", "name"))

        # Ensure wishlist exists
        wishlist, _ = PropertyWishlist.objects.get_or_create(
            created_by=user,
            defaults={"name": "My Wishlist", "description": "My favorite properties"},
        )

        # Auto-create profile if missing
        profile_id = None
        user_type = getattr(user, "user_type", None)
        profile_model_map = {
            "buyer": "BuyerProfile",
            "seller": "SellerProfile",
            "agent": "AgentProfile",
            "developer": "DeveloperProfile",
            "admin": "AdminProfile",
        }

        model_name = profile_model_map.get(user_type)
        if model_name:
            try:
                from django.apps import apps
                ProfileModel = apps.get_model("authapp", model_name)
                profile, created = ProfileModel.objects.get_or_create(user=user)
                profile_id = profile.id
                if created:
                    print(f"✅ Created new {model_name} for {user.email}")
            except Exception as e:
                print(f"❌ Profile creation failed for {user.email}: {e}")

        # Build response
        data = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user_id": user.id,
            "email": user.email,
            "name": user.get_full_name(),
            "first_name": user.first_name,
            "last_name": user.last_name,
            "groups": groups,
            "user_type": user_type,
            "wishlist_id": wishlist.id,
        }
        if profile_id:
            data["profile_id"] = profile_id

        return Response(data, status=200)

    @extend_schema(
        request=RefreshTokenSerializer,
        summary="Refresh access token",
    )
    @action(detail=False, methods=["post"], url_path="refresh-token")
    def refresh_token(self, request):
        serializer = RefreshTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            token = RefreshToken(serializer.validated_data["refresh"])
            return Response({"access": str(token.access_token)}, status=200)
        except TokenError:
            return Response({"error": "Invalid or expired refresh token"}, status=400)

    @extend_schema(
        request=LogoutSerializer,
        summary="Logout (blacklist refresh token)",
    )
    @action(detail=False, methods=["post"])
    def logout(self, request):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            token = RefreshToken(serializer.validated_data["refresh"])
            token.blacklist()
            return Response({"success": "Logged out successfully"}, status=200)
        except TokenError:
            return Response({"error": "Invalid or expired refresh token"}, status=400)
