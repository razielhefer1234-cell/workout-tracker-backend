from workouts.models import Workout, WorkoutExercise, WorkoutSession
from rest_framework import serializers

class WorkoutExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutExercise
        fields = '__all__'
        read_only_fields = ("workout", "exercise",)

class WorkoutSerializer(serializers.ModelSerializer):
    workout_exercises = WorkoutExerciseSerializer(many=True, read_only=True)
    
    class Meta:
        model = Workout
        fields = ["id", "name", "created_at", "description", "user", "workout_exercises"]
        read_only_fields = ("user",)

class WorkoutSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutSession
        fields = '__all__'
        read_only_fields = ("workout",)
        
