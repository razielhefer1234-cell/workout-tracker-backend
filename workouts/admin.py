from django.contrib import admin
from .models import Workout, WorkoutExercise, WorkoutSession, ExerciseResult

class WorkoutExerciseInline(admin.TabularInline):
    model = WorkoutExercise
    extra = 0

@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "created_at")
    search_fields = ("name", "user__email")
    list_filter = ("created_at",)
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)
    inlines = [WorkoutExerciseInline]

@admin.register(WorkoutExercise)
class WorkoutExerciseAdmin(admin.ModelAdmin):
    list_display = ("workout", "exercise", "order", "sets", "reps", "weight", "rest_seconds")
    search_fields = ("workout__name", "exercise__name", "workout__user__email")
    list_filter = ("exercise",)
    ordering = ("workout", "order")

@admin.register(WorkoutSession)
class WorkoutSessionAdmin(admin.ModelAdmin):
    list_display = ("workout", "scheduled_at", "status", "completed_at", "total_duration")
    search_fields = ("workout__name", "workout__user__email", "note")
    list_filter = ("status", "scheduled_at")
    ordering = ("-scheduled_at",)
    readonly_fields = ("completed_at",)

    def get_readonly_fields(self, request, obj=None):
        if obj is not None and obj.status == "completed":
            return (
                "workout",
                "scheduled_at",
                "status",
                "completed_at",
                "note",
                "total_duration",
            )
        if obj is not None and obj.status == "cancelled":
            return (
                "status",
                "completed_at"
            )
        return self.readonly_fields

@admin.register(ExerciseResult)
class ExerciseResultAdmin(admin.ModelAdmin):
    list_display = ("workout_session", "exercise", "exercise_order", "sets_completed", "reps_completed", "weight_completed", "duration")
    search_fields = ("exercise__name", "workout_session__workout__name", "workout_session__workout__user__email")
    list_filter = ("exercise", "workout_session__status")
    ordering = ("workout_session_id", "exercise_order")
    readonly_fields = ("exercise", "exercise_order")

    def get_readonly_fields(self, request, obj=None):
        if obj is not None:
            return (
                "sets_completed",
                "reps_completed",
                "exercise",
                "workout_session",
                "workout_exercise",
                "exercise_order",
                "weight_completed",
                "duration"
            )
        return self.readonly_fields