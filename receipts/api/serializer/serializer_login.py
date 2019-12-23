from rest_framework import serializers
from django.contrib.auth.models import User

class UserLoginSerializer(serializers.ModelSerializer):
    """
    User serializer for login purpose
    """
    class Meta:
        model = User
        fields = ("username", 'password')


class TokenSerializer(serializers.Serializer):
    """
    JWT Token serializer
    """
    token = serializers.CharField(max_length=255)