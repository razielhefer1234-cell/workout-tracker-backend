from django.urls import path
from . import views

urlpatterns = [
    path("me-info/", views.current_user, name="user_info"),
    path("logout/", views.logout, name="logout"),
]