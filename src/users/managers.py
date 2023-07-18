from django.contrib.auth.base_user import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        print('====1.1====')
        if not email:
            raise ValueError("The Email must be str")
        print('====1.2====')
        email = self.normalize_email(email)
        print('====1.3====')
        user = self.model(email=email)
        print('====1.4====')
        user.set_password(password)
        print('====1.5====')
        # extra_fields.setdefault("is_superuser", False)
        # extra_fields.setdefault("is_staff", False)
        # extra_fields.setdefault("is_active", True)
        user.save()
        print('====1.6====')
        return user

    def create_superuser(self, email, password, **extra_fields):
        # extra_fields.setdefault("is_superuser", True)
        # extra_fields.setdefault("is_staff", True)
        # extra_fields.setdefault("is_active", True)
        if not email:
            raise ValueError("The Email must be str")
        
        email = self.normalize_email(email)
        
        user = self.model(email=email)
        
        user.set_password(password)

        # user.save()
        # user = self.create_user(email, password, **extra_fields)
        print('====2====')
        user.is_superuser = True
        print('====3====')
        user.is_staff = True
        print('====4====')
        user.is_active = True
        user.is_simple_user = False
        user.is_builder = False
        print('====5====')
        user.save()
        print('====6====')
        # return self.create_user(email, password, **extra_fields)
        return user