from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from django.contrib.auth.password_validation import validate_password
from .models import MyUser
from rest_framework.permissions import AllowAny
from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import IntegrityError
from drf_spectacular.utils import extend_schema, OpenApiExample
from .serializers import SignUpRequestSerializer, SignUpResponseSerializer, CurrentUserResponseSerializer, LogoutRequestSerializer, LogoutResponseSerializer

@extend_schema(responses={200: CurrentUserResponseSerializer})
@api_view(["GET"])
def current_user(request):
    return Response({
        "id": request.user.id,
        "email": request.user.email,
        "first_name": request.user.first_name,
        "last_name": request.user.last_name,
    }, status=200)

@extend_schema(request=LogoutRequestSerializer, responses={200: LogoutResponseSerializer})
@api_view(["POST"])
def logout(request):
    refresh_token_string = request.data.get("refresh")
    if not refresh_token_string:
        return Response({"detail": "Refresh token is required."}, status=400)
    try:
        token = RefreshToken(refresh_token_string)
    except TokenError:
        return Response({"detail": "Invalid or expired refresh token."}, status=400)
    token.blacklist()
    return Response({"detail": "Logged out successfully."}, status=200)

@extend_schema(
    request=SignUpRequestSerializer,
    responses={201: SignUpResponseSerializer},
    examples=[
        OpenApiExample(
            "Sign-up request",
            value={
                "email": "user@example.com",
                "password": "StrongPassword123!",
                "first_name": "John",
                "last_name": "Smith",
            },
            request_only=True,
        ),
        OpenApiExample(
            "Successful sign-up",
            value={
                "detail": "Account created. Please log in.",
            },
            response_only=True,
            status_codes=[201],
        ),
    ],
)
@api_view(["POST"])
@permission_classes([AllowAny])
def sign_up(request):
    email = request.data.get("email")
    first_name = request.data.get("first_name")
    last_name = request.data.get("last_name")
    password = request.data.get("password")

    if not(email and first_name and last_name and password):
        return Response({"detail": "You need to fill all the fields"}, status=400)

    try:
        user = MyUser.objects.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
        )
    except DjangoValidationError as error:
        if hasattr(error, "message_dict"):
            return Response(error.message_dict, status=400)
        return Response({"password": error.messages}, status=400)
    except IntegrityError:
        return Response({"email": "This email is already registered."}, status=400)

    return Response({"detail": "Account created. Please log in."}, status=201)

    
    

