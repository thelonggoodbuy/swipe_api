from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


from .models import CustomUser

# ========================================================================
# =======================CUSTOM VALIDATORS================================
# ========================================================================

class UniqueEmailValidator(UniqueValidator):
    message = 'Email має бути унікальним.'




# ========================================================================
# =============AUTHENTICATION AND AUHORZATION SERIALIZERS=================
# ========================================================================

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
    Serializer class for registration requests 
    and create a new simple user
    """
    
    email = serializers.CharField(validators=[UniqueEmailValidator(queryset=CustomUser.objects.all())])
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
    """
    Serializator class for retreave, update and partly update simple user
    """

    email = serializers.CharField(required=False, validators=[UniqueEmailValidator(queryset=CustomUser.objects.all())])

    class Meta:
        model = CustomUser
        fields = ("id", "first_name", "second_name",
                  "phone", "email", "nontifications_status")


class UserChangePasswordRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ("id",)



class SimpleUserChangePasswordSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ("password", "confirm_password")

    def validate(self, data):
        password = data['password']
        confirm_password = data['confirm_password']
        # match password:
        #     case data['confirm_password']:
        #         return user
        #     case _:
        #         raise serializers.ValidationError("Помилка в емейлі або в паролі")
        if password == confirm_password:
            # return self.instance
            data.pop('confirm_password')
            return data
        else:
             raise serializers.ValidationError("Паролі повинні співпадати")
        
    # def update(self, instance, validated_data):

    #     instance.set_password(validated_data['password'])
    #     instance.save()

    #     return instance