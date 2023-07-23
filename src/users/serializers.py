from django.contrib.auth import authenticate
from rest_framework import serializers

from .models import CustomUser






class UserLoginSerializer(serializers.Serializer):
    """
    Serializer class to authenticate users with email and password
    """

    email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and not user.is_in_blacklist:
            return user
        raise serializers.ValidationError("Incorrect Credential")
    

class UserRegistrationSerializer(serializers.Serializer):
    """
    Serializer class for serializing registration requests 
    and create a new simple user
    """
    
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)
    is_simple_user = serializers.CharField(default=True)

    def save(self, email, password, is_simple_user):
        user =  CustomUser.objects.create_user(
            email,
            password,
            is_simple_user
        )
        return user

class SimpleUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ("id", "first_name", "second_name",
                  "phone", "email", "nontifications_status")