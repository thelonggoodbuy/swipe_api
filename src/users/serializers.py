from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from drf_extra_fields.fields import Base64ImageField

from .models import CustomUser, Subscription

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


from drf_spectacular.utils import extend_schema_serializer, OpenApiExample


class SimpleUserSubscriptionSerializer(serializers.ModelSerializer):
    subscription_last_date = serializers.DateField(format="%d.%m.%Y", input_formats=["%d.%m.%Y"])
    # is_extend_comand = serializers.BooleanField(default=False)
    class Meta:
        model = Subscription
        # fields = ("subscription_last_date", "is_auto_renewal", "is_extend_comand")
        fields = ("subscription_last_date", "is_auto_renewal")



@extend_schema_serializer(
    examples = [
         OpenApiExample(
            'Testing example #1 with testing values.',
            summary='Testing example #1',
            description='Warning: such photo value can`t be validated!',
            value={
                    "first_name": "Example_Name",
                    "second_name": "Example_Second_Name",
                    "photo": "put_per_image_in_base64_form",
                    "phone": "+380631111111",
                    "email": "example_user@email.com",
                    "nontifications_status": "for_user",
                    "agent_email": "example_agent@example.com",
                    "agent_phone": "+380632222222",
                    "agent_first_name": "Example_Agent_Name",
                    "agent_second_name": "Example_Agent_Second_Name",
                    "subscription": {
                        "subscription_last_date": "29.12.2023",
                        "is_auto_renewal": True
                    }
            },
            request_only=True, # signal that example only applies to requests
        ),


    ]
)
class SimpleUserSerializer(serializers.ModelSerializer):
    """
    Serializator class for retreave, update and partly update simple user
    """

    email = serializers.CharField(required=False, validators=[UniqueEmailValidator(queryset=CustomUser.objects.all())])
    photo = Base64ImageField(required=False)

    subscription = SimpleUserSubscriptionSerializer(required=False)

    class Meta:
        model = CustomUser
        fields = ("id", "first_name", "second_name", "photo",
                  "phone", "email", "nontifications_status",
                  "agent_email", "agent_phone", "agent_first_name",
                  "agent_second_name", "subscription")

    def update(self, instance, validated_data):

        subscription_data = validated_data.pop('subscription')
        custom_user_obj = instance

        for (field_name, field_value) in validated_data.items():
            setattr(custom_user_obj, field_name, field_value)
        custom_user_obj.save()

        subscription_obj = custom_user_obj.subscription

        for (field_name, field_value) in subscription_data.items():
            setattr(subscription_obj, field_name, field_value)
        subscription_obj.save()

        return custom_user_obj



class UserChangePasswordRequestSerializer(serializers.ModelSerializer):
    """
    Serializer for request to change password.
    """
    class Meta:
        model = CustomUser
        fields = ("id",)



class SimpleUserChangePasswordSerializer(serializers.ModelSerializer):
    """
    request for changing password
    """

    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ("password", "confirm_password")

    def validate(self, data):
        password = data['password']
        confirm_password = data['confirm_password']
        if password == confirm_password:
            data.pop('confirm_password')
            return data
        else:
             raise serializers.ValidationError("Паролі повинні співпадати")
        