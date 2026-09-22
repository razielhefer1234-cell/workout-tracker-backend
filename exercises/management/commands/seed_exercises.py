from django.core.management.base import BaseCommand
from exercises.models import Exercise

Exercises = [
    "Push-Up",
    "Squat",
    "Plank",
    "Pull-Up",
    "Lunge",
    "Burpee",
    "Sit-Up",
    "Deadlift",
    "Bench Press",
    "Shoulder Press",
]

class Command(BaseCommand):
    def handle(self, *args, **options):
        for exercise in Exercises:
            Exercise.objects.get_or_create(name=exercise)