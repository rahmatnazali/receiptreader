from rest_framework import serializers
from receiptreader.models import ProcessedReceipt, RawReceipt, Image
from django.contrib.auth.models import User
from rest_framework_jwt.settings import api_settings

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


# receipt model
class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'

class RawReceiptSerializer(serializers.ModelSerializer):
    image_set = ImageSerializer(many=True)
    class Meta:
        model = RawReceipt
        fields = '__all__'
