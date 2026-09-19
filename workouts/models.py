from django.db import models
from accounts.models import MyUser

# Create your models here.
class Workout(models.Model):
    name = models.CharField(max_length=30, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    user_id = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = "Workout"
        verbose_name_plural = "Workouts"
        db_table = "Workout"
