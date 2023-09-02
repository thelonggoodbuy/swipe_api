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


@pytest.fixture
def api_client_fixture():
    client = APIClient()
    return client