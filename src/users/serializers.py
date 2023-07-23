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
    Serializer class to serialize registration requests 
    and create a new simple user
    """
    
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)
    is_simple_user = serializers.CharField(default=True)
    # class Meta:
    #     model = CustomUser
    #     fields = ("id", "email", "password", "is_simple_user")
    #     extra_kwargs = {"password": {"write_only": True}}

    def save(self, email, password, is_simple_user):
        user =  CustomUser.objects.create_user(
            email,
            password,
            is_simple_user
        )
        return user

        # def create(self, email, password, is_simple_user):
        #     user =  CustomUser.objects.create_user(
        #         email,
        #         password,
        #         True
        #     )
        #     return user
        #     # return CustomUser.objects.create_user(**validated_data)