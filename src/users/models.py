from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.mail import send_mail

from .managers import CustomUserManager

from ads.models import Ads, Accomodation


class CustomUser(AbstractBaseUser, PermissionsMixin):
    NONTIFICATION_STATUS = (
        ("for_user", "оповещения пользователю"),
        ("for_user_and_agent", "оповещения пользователю и агенту"),
        ("for_agent", "оповещению агенту"),
        ("disabled", "отключить оповещения"),
    )
    username = None
    email = models.EmailField(unique=True)
    # password = models.CharField(max_length=200, blank=True)
    is_superuser = models.BooleanField(default=False)
    is_simple_user = models.BooleanField(default=False)
    is_builder = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_activated = models.BooleanField(default=False)
    first_name = models.CharField(max_length=200, blank=True, null=True)
    second_name = models.CharField(max_length=200, blank=True, null=True)
    photo = models.ImageField(null=True, blank=True, upload_to="galery/")
    phone = models.CharField(max_length=200, blank=True, null=True)
    # agent = models.ForeignKey("Agent", on_delete=models.SET_NULL, blank=True, null=True)
    agent_email = models.EmailField(max_length=200, blank=True, null=True)
    agent_phone = models.CharField(max_length=200, blank=True, null=True)
    agent_first_name = models.CharField(max_length=200, blank=True, null=True)
    agent_second_name = models.CharField(max_length=200, blank=True, null=True)
    nontifications_status = models.CharField(max_length=200, choices=NONTIFICATION_STATUS, default="for_user_and_agent")
    change_call_to_agent = models.BooleanField(default=False)
    is_in_blacklist = models.BooleanField(default=False)
    subscription = models.OneToOneField('Subscription', on_delete=models.SET_NULL, null=True, blank=True)
    favourite_adds = models.ManyToManyField(Ads, blank=True)
    favourite_accomodations = models.ManyToManyField(Accomodation, blank=True)

    # username = None
    USERNAME_FIELD = "email"

    # EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def activate_user(self):
        self.is_activated = True
        self.save()
        return self
    
    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)
    

class Subscription(models.Model):
    subscription_last_date = models.DateField(null=True, blank=True, default=None)
    is_auto_renewal = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)



class Message(models.Model):
    from_user = models.ForeignKey("CustomUser", on_delete=models.SET_NULL, blank=True, null=True, related_name="user_message_sender")
    to_user = models.ForeignKey("CustomUser", on_delete=models.SET_NULL, blank=True, null=True, related_name="user_message_reseiver")
    date_and_time = models.DateTimeField()
    reading_status = models.BooleanField(default=False)
    message_text = models.TextField()
    
    
class Notary(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    surname = models.CharField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField()