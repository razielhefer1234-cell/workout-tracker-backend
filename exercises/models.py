from django.db import models

# Create your models here.
class Exercise(models.Model):
    name = models.CharField(max_length=40, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ["name"]
        verbose_name = "Exercise"
        verbose_name_plural = "Exercises"
        db_table = "Exercises"
