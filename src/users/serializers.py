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
        # if user and not user.is_in_blacklist and user.is_activated:
        #     return user
        # elif user and not user.is_in_blacklist and user.is_activated == False:
        #     raise serializers.ValidationError("Профіль не активовано через електронну пошту")
        # elif user and user.is_in_blacklist:
        #     raise serializers.ValidationError("Профіль в чорному списку")
        # else:
        #     raise serializers.ValidationError("Помилка в емейлі або в паролі")
        match user:
            case CustomUser(is_in_blacklist=False, is_activated=True):
                return user
            case CustomUser(is_in_blacklist=False, is_activate=False):
                raise serializers.ValidationError("Профіль не активовано через електронну пошту")
            case CustomUser(is_in_blacklist=True):
                raise serializers.ValidationError("Профіль в чорному списку")
            case _:
                raise serializers.ValidationError("Помилка в емейлі або в паролі")
            

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
        