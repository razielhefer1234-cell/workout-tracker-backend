from django.db import models
from accounts.models import MyUser
from django.core.validators import MinValueValidator
from exercises.models import Exercise
from django.conf import settings

# Create your models here.
class Workout(models.Model):
    name = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="workouts",
        related_query_name="workout",
    )

    exercises = models.ManyToManyField(
        Exercise,
        through="WorkoutExercise",
        related_name="workouts",
        related_query_name="workout",
    )
    
    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = "Workout"
        verbose_name_plural = "Workouts"
        db_table = "Workout"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "name"],
                name="unique_workout_name_per_user",
            )
        ]

class WorkoutExercise(models.Model):
    order = models.IntegerField(validators=[MinValueValidator(1)])
    sets = models.IntegerField(validators=[MinValueValidator(1)])
    reps = models.IntegerField(validators=[MinValueValidator(1)])
    rest_seconds = models.IntegerField(validators=[MinValueValidator(1)])
    workout = models.ForeignKey(
        Workout,
        related_name="workout_exercises",
        related_query_name="workout_exercise",
        on_delete=models.CASCADE,
    )
    exercise = models.ForeignKey(
        Exercise,
        on_delete=models.CASCADE,
        related_name="workout_exercises",
        related_query_name="workout_exercise",
    )

    def __str__(self):
        return f"{self.workout.name} — {self.exercise.name}"

    class Meta:
        ordering = ["workout", "order"]
        verbose_name = "WorkoutExercise"
        verbose_name_plural = "WorkoutExercises"
        db_table = "WorkoutExercise"
        constraints = [
            models.UniqueConstraint(
                fields=["workout", "order"],
                name="unique_order_per_workout",
            ) 
        ]