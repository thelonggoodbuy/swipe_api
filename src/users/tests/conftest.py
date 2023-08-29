import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import CustomUser
from django.conf import settings
import environ
import os
env = environ.Env()
environ.Env.read_env(env_file=os.path.join(settings.BASE_DIR, ".env.dev"))



@pytest.fixture(scope='function')
def django_db_setup():
    settings.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env("POSTGRES_TEST_DB"),
        'USER': env("POSTGRES_TEST_USER"),
        'PASSWORD': env("POSTGRES_TEST_PASSWORD"),
        "HOST": env("POSTGRES_HOST"),
        "PORT": env("POSTGRES_PORT"),
    }


# --------------------SIMPLE--USER-REGISTRATION-AND-AUTHENTICATION-FIXTURES------------------
@pytest.fixture
def create_user_and_authenticate_fixture(db):
    payload = {
        "email": "test123_email@mail.com",
        "is_simple_user": True,
        "is_activated": True,
    }
    test_user = CustomUser(**payload)
    test_user.set_password("test_password")
    test_user.save()
    client = APIClient()
    refresh = RefreshToken.for_user(test_user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return client



@pytest.fixture
def api_client_fixture():
    client = APIClient()
    return client



@pytest.fixture
def create_user_without_authentication_fixture(db):
    new_user = CustomUser.objects.create(
        email='test123_email@mail.com',
        is_simple_user = True,
        is_activated = True,
        )
    new_user.set_password("test_password")
    client = APIClient()
    return client

# --------------------ADMIN--USER-REGISTRATION-AND-AUTHENTICATION-FIXTURES------------------
@pytest.fixture
def create_admin_user_and_authenticate_fixture(db):
    payload = {
        "email": "test123_email@mail.com",
        "is_superuser": True,
        "is_staff": True,
        "is_activated": True,
    }
    test_user = CustomUser(**payload)
    test_user.set_password("test_password")
    test_user.save()
    client = APIClient()
    refresh = RefreshToken.for_user(test_user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return client

# ---------------------------USER-SUBSCRIPTION-FIXTURES----------------------------------

from users.models import Subscription
from django.utils import timezone
from dateutil.relativedelta import relativedelta




@pytest.fixture
def create_user_with_subscription_fixture(db):
    payload = {
        "email": "test123_email@mail.com",
        "is_simple_user": True,
        "is_activated": True,
    }
    test_user = CustomUser(**payload)
    test_user.set_password("test_password")
    

    new_subscription = Subscription()
    new_subscription.is_auto_renewal = False

    new_subscription.subscription_last_date = timezone.now()
    new_subscription.is_active = True
    new_subscription.save()
    test_user.subscription = new_subscription
    test_user.save()

    client = APIClient()
    refresh = RefreshToken.for_user(test_user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return client
