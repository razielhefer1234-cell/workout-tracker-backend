from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import MyUser

@admin.register(MyUser)
class MyUserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal information", {"fields": ("first_name", "last_name")}),
        ("Permissions", {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            )
        }),
        ("Important dates", {"fields": ("last_login", "creation")}),
    )
    add_fieldsets = (
        (None, {"fields": ("email", "password1", "password2")}),
        (None, {"fields": ("first_name", "last_name")}),
        (None, {
            "fields": (
                "is_active",
                "is_staff",
            )
        }),
    )
    list_display = ("email", "first_name", "last_name", "is_active", "is_staff")
    ordering = ("email",)
    search_fields = ("email", "first_name", "last_name")
    list_filter = ("is_staff", "is_active", "is_superuser")
    readonly_fields = ("creation", "last_login")

