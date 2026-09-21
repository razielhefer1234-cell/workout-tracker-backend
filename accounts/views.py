from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

@api_view(["GET"])
def current_user(request):
    return Response({
        "id": request.user.id,
        "email": request.user.email,
        "first_name": request.user.first_name,
        "last_name": request.user.last_name,
    }, status=200)

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
