from django.contrib import admin
from .models import Exercise

@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")
    search_fields = ("name",)
    ordering = ("name",)
    readonly_fields = ("created_at",)


