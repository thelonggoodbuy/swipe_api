from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


from .managers import CustomUserManager

from ads.models import Ads, Accomodation


class User(AbstractBaseUser, PermissionsMixin):
    NONTIFICATION_STATUS = (
        ("оповещения пользователю", "for_user"),
        ("оповещения пользователю и агенту", "for_user_and_agent"),
        ("оповещению агенту", "for_agent"),
        ("отключить оповещения", "disabled"),
    )
    username = None
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=200, blank=True)
    is_superuser = models.BooleanField()
    is_simple_user = models.BooleanField()
    is_builder = models.BooleanField()
    first_name = models.CharField(max_length=200, blank=True, null=True)
    second_name = models.CharField(max_length=200, blank=True, null=True)
    photo = models.ImageField(null=True, blank=True, upload_to="galery/")
    phone = models.CharField(max_length=200, blank=True, null=True)
    agent = models.ForeignKey("Agent", on_delete=models.SET_NULL, blank=True, null=True)
    nontifications_status = models.CharField(max_length=200, choices=NONTIFICATION_STATUS, default=NONTIFICATION_STATUS[1][1])
    change_call_to_agent = models.BooleanField(default=False)
    is_in_blacklist = models.BooleanField(default=False)
    subscription = models.OneToOneField('Subscription', on_delete=models.SET_NULL, null=True, blank=True)
    favourite_adds = models.ManyToManyField(Ads)
    favourite_accomodations = models.ManyToManyField(Accomodation)

    # username = None
    USERNAME_FIELD = "email"

    # EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
    

class Subscription(models.Model):
    Subscription_last_date = models.DateField()
    
    
class Agent(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    surname = models.CharField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField()
    

class Message(models.Model):
    from_user = models.ForeignKey("User", on_delete=models.SET_NULL, blank=True, null=True, related_name="user_message_sender")
    to_user = models.ForeignKey("User", on_delete=models.SET_NULL, blank=True, null=True, related_name="user_message_reseiver")
    date_and_time = models.DateTimeField()
    reading_status = models.BooleanField(default=False)
    
    
class Notary(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    surname = models.CharField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField()
