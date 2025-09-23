from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str
from drf_spectacular.utils import extend_schema
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from authapp.serializers.password_reset import (
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
)

User = get_user_model()


class PasswordResetViewSet(viewsets.ViewSet):
    @extend_schema(
        request=PasswordResetRequestSerializer,
        responses={"200": {"message": "Password reset email sent"}},
        summary="Request password reset",
        description="Sends a password reset email to the user"
    )
    @action(detail=False, methods=["post"])
    def request_reset(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"error": "User with this email does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Generate token
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        reset_link = f"http://localhost:3000/reset-password/{uid}/{token}/"  
        # 👆 You can point this to your frontend reset page

        # Send email (dummy example)
        send_mail(
            subject="Password Reset Request",
            message=f"Click here to reset your password: {reset_link}",
            from_email="noreply@example.com",
            recipient_list=[email],
            fail_silently=True,
        )

        return Response({"message": "Password reset email sent"}, status=status.HTTP_200_OK)
    
    
    @extend_schema(
        request=PasswordResetConfirmSerializer,
        responses={"200": {"message": "Password has been reset successfully"}},
        summary="Confirm password reset",
        description="Resets the user's password using the provided token"
    )
    @action(detail=False, methods=["post"])
    def confirm_reset(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        uidb64 = serializer.validated_data["uidb64"]
        token = serializer.validated_data["token"]
        new_password = serializer.validated_data["new_password"]

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError, TypeError):
            return Response({"error": "Invalid link"}, status=status.HTTP_400_BAD_REQUEST)

        if not default_token_generator.check_token(user, token):
            return Response({"error": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        return Response({"message": "Password has been reset successfully"}, status=status.HTTP_200_OK)
