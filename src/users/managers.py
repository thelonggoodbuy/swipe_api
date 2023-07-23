from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password


class CustomUserManager(BaseUserManager):
    # def create_user(self, email, password, is_superuser, is_staff, is_simple_user):
    #     if not email:
    #         raise ValueError("The Email must be str")
    #     email = self.normalize_email(email)
    #     user = get_user_model(email=email)
    #     user.set_password(password)
    #     user.is_superuser =  False
    #     user.is_staff = False
    #     user.is_simple_user = True
    #     return user

    def create_user(self, email, password, is_simple_user):
        if not email:
            raise ValueError("The Email must be str")
        email = self.normalize_email(email)
        user = self.model(email=email, password=password, is_simple_user=is_simple_user)
        user.password = make_password(password)
        # user.is_superuser =  False
        # user.is_staff = False
        # user.is_simple_user = True
        print('You use manager for simple user!!!')
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The Email must be str")
        email = self.normalize_email(email)
        user = self.model(email=email)
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.is_simple_user = False
        user.is_builder = False
        user.save()
        return user