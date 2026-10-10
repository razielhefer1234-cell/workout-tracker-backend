from rest_framework import serializers

class SignUpRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=30)

class SignUpResponseSerializer(serializers.Serializer):
    detail = serializers.CharField()

class CurrentUserResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=30)

class LogoutRequestSerializer(serializers.Serializer):
    refresh = serializers.CharField(write_only=True)

class LogoutResponseSerializer(serializers.Serializer):
    detail = serializers.CharField()