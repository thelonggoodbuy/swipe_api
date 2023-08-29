from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from drf_extra_fields.fields import Base64ImageField
from drf_spectacular.utils import extend_schema_serializer, OpenApiExample
from django.utils import timezone
from django.db.models import Q
from faker import Faker



from django.utils.timezone import now
from dateutil.relativedelta import relativedelta


from .models import CustomUser, Subscription, Notary, Message

fake = Faker()


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
        custom_user_obj = instance
        for (field_name, field_value) in validated_data.items():
            setattr(custom_user_obj, field_name, field_value)
        custom_user_obj.save()
        try:
            subscription_data = validated_data.pop('subscription')
            subscription_obj = custom_user_obj.subscription

            for (field_name, field_value) in subscription_data.items():
                setattr(subscription_obj, field_name, field_value)
            subscription_obj.save()
        except KeyError:
            pass

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
        




class SimpleUserMessageCreateAndListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ("message_text", )

    def create(self, validated_data):
        new_message = self.Meta.model(**validated_data)
        admin = CustomUser.objects.filter(is_superuser=True).first()
        new_message.to_user = admin
        request = self.context.get("request")
        new_message.from_user = request.user
        new_message.reading_status = False
        new_message.date_and_time = timezone.now()
        new_message.save()
        response_message = self.Meta.model.objects.create(
                            from_user=admin,
                            to_user=request.user,
                            date_and_time = timezone.now(),
                            message_text=fake.text())
        response_message.save()
        return new_message




class NotarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Notary
        fields = ['name', 'surname', 'phone', 'email']




class SimpleUserUpdateSubscriptionSerializer(serializers.ModelSerializer):
    subscription_last_date = serializers.SerializerMethodField()
    is_auto_renewal = serializers.BooleanField(default=False)
    is_prolonging = serializers.BooleanField(default=False)


    class Meta:
        model = CustomUser
        fields = ['subscription_last_date', 'is_auto_renewal', 'is_prolonging']
        read_only_fields = ['subscription_last_date',]

    
    def get_subscription_last_date(self, obj):
        subscription_data = obj.subscription
        if subscription_data:
            data = {'last_date': subscription_data.subscription_last_date,
                    'auto_renewal': subscription_data.is_auto_renewal}
        else:
            data = {'last_date': 'Ви не підписані',
                    'auto_renewal': 'Ви не підписані'}
        return data
    

    def save(self, instance, validated_data):
        if instance.subscription:
            if validated_data.get('is_auto_renewal'):
                instance.subscription.is_auto_renewal = validated_data.get('is_auto_renewal')

            if validated_data.get('is_prolonging') and validated_data.get('is_prolonging') == True:
                instance.subscription.subscription_last_date = instance.subscription.subscription_last_date + relativedelta(months=1)
                instance.subscription.is_active = True
            
            instance.subscription.save()
            instance.save()

        if instance.subscription == None:
            new_subscription = Subscription()
            if validated_data.get('is_auto_renewal'):
                new_subscription.is_auto_renewal = validated_data.get('is_auto_renewal')

            if validated_data.get('is_prolonging') and validated_data.get('is_prolonging') == True:
                new_subscription.subscription_last_date = timezone.now() + relativedelta(months=1)

            new_subscription.is_active = True
            new_subscription.save()
            instance.subscription = new_subscription
            instance.save()

        return instance
