from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(["GET"])
def current_user(request):
    return Response({
        "id": request.user.id,
        "email": request.user.email,
        "first_name": request.user.first_name,
        "last_name": request.user.last_name,
    }, status=status.HTTP_200_OK)