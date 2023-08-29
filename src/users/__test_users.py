import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.conf import settings
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from faker import Faker
from rest_framework_simplejwt.tokens import RefreshToken

from .models import CustomUser, Message, Notary
from .tokens import user_activation_token

fake = Faker()


# ========================================FIXTURE==============================
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
def api_client():
    client = APIClient()
    return client


# @pytest.fixture
# def create_user_payload():
#     payload = {
#         "email": "test_user@gmail.com",
#         "is_simple_user": True
#     }
#     test_user = CustomUser(**payload)
#     test_user.set_password("test_password_123!@")
#     test_user.save()
#     return test_user

@pytest.fixture
def create_user_and_login_payload():
    payload = {
        "email": "test_loggined_user@gmail.com",
        "is_simple_user": True,
        "is_activated": True,
    }
    test_user = CustomUser(**payload)
    test_user.set_password("test_loggined_password_123!@")
    test_user.save()
    client = APIClient()
    refresh = RefreshToken.for_user(test_user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return client

# @pytest.fixture
# def create_admin_payload():
#     payload = {
#         "email": "test_admin_user@gmail.com",
#         "is_superuser": True,
#         "is_activated": True,
#     }
#     test_user = CustomUser(**payload)
#     test_user.set_password("test_admin_password_123!@")
#     test_user.save()
#     client = APIClient()
#     refresh = RefreshToken.for_user(test_user)
#     client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
#     return client

# *****************************************************************************
# *****************************************************************************
# *****************************************************************************

@pytest.fixture
def create_user_new_fixture(db):
    new_user = CustomUser.objects.create(
        password='test_email@mail.com',
        email='test123_email@mail.com'
        )
    
    client = APIClient()
    refresh = RefreshToken.for_user(new_user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return client
#    return make_user_new_fixture

# *****************************************************************************
# *****************************************************************************
# *****************************************************************************
# ====================================END=FIXTURE==============================

# ====================================TESTS====================================
# *****************************************************************************
# *****************************************************************************
# *****************************************************************************
# @pytest.mark.django_db
# def test_user_detail(api_client, create_user_new_fixture):

#     user = CustomUser.objects.get(email="test123_email@mail.com")
#     url = f'/users/simple_user_update_and_detail/{user.id}/'
#     response = create_user_new_fixture.get(url, format='json')
#     assert response.status_code == 200


# *****************************************************************************
# *****************************************************************************
# *****************************************************************************

@pytest.mark.django_db
def test_simple_user_registration(api_client, db):

    print('================')
    print(db)
    print('================')

    # Testing creating a simple user entrypoint
    # without email confirmation.
    url = '/users/auth/register_simple_user/'
    payload = {
        "email": "test_user@gmail.com",
        "password": "test_password_123!@",
        "is_simple_user": True,
    }
    response = api_client.post(url, payload, response='json')
    assert response.status_code == status.HTTP_201_CREATED
    print(CustomUser.objects.all())
    assert CustomUser.objects.count() == 1



@pytest.mark.django_db
def test_simple_user_activation_registration(api_client):
    # Testing email confirmation with creation simple user.
    url = '/users/auth/register_simple_user/'
    payload = {
        "email": "test_user@gmail.com",
        "password": "test_password_123!@",
        "is_simple_user": True,
    }
    response = api_client.post(url, payload, response='json')
    user = CustomUser.objects.get(email='test_user@gmail.com')
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = user_activation_token.make_token(user)
    activation_url = f'/users/auth/activate_simple_user/{uid}/{token}/'
    response_for_activation = api_client.get(activation_url)
    user.refresh_from_db()
    assert user.is_activated == True
    assert response_for_activation.status_code == 200


# @pytest.mark.django_db
# def test_get_simple_user_data(create_user_and_login_payload):
#     # Test retreave(GET) simple user entrypoint.

#     user = CustomUser.objects.get(email="test_loggined_user@gmail.com")
#     url = f'/users/simple_user_update_and_detail/{user.id}/'
#     response = create_user_and_login_payload.get(url, format='json')
#     assert response.status_code == 200


@pytest.mark.django_db
def test_put_simple_user_data(create_user_and_login_payload):
    # Test updating(PUT) simple user entrypoint.

    payload = {
        'first_name': fake.name(),
        'second_name': fake.name()
    }
    user = CustomUser.objects.get(email="test_loggined_user@gmail.com")
    url = f'/users/simple_user_update_and_detail/{user.id}/'
    response = create_user_and_login_payload.put(url, payload, format='json')
    user.refresh_from_db()
    assert user.first_name == payload['first_name']
    assert user.second_name == payload['second_name']
    assert user.email == 'test_loggined_user@gmail.com'
    assert response.status_code == 200


@pytest.mark.django_db
def test_path_simple_user_data(create_user_and_login_payload):
    # Test updating(PATCH) simple user entrypoint.

    payload = {
        'first_name': fake.name(),
        'second_name': fake.name()
    }
    user = CustomUser.objects.get(email="test_loggined_user@gmail.com")
    url = f'/users/simple_user_update_and_detail/{user.id}/'
    response = create_user_and_login_payload.patch(url, payload, format='json')
    user.refresh_from_db()
    assert user.first_name == payload['first_name']
    assert user.second_name == payload['second_name']
    assert user.email == 'test_loggined_user@gmail.com'
    assert response.status_code == 200


@pytest.mark.django_db
def test_change_password_request(create_user_and_login_payload):
    # Test GET request for changing password
    user = CustomUser.objects.get(email="test_loggined_user@gmail.com")
    url = f'/users/user_change_password_request/{user.id}/'
    response = create_user_and_login_payload.get(url)
    assert response.status_code == 201


@pytest.mark.django_db
def test_change_password(create_user_and_login_payload):
    # Test POST request to change password throw
    # token (in users app this token is used for
    # email change password confirmation)
    user = CustomUser.objects.get(email="test_loggined_user@gmail.com")
    old_password = user.password
    url = f'/users/user_change_password_request/{user.id}/'
    create_user_and_login_payload.get(url)
    uid = urlsafe_base64_encode(force_bytes(user.id))
    token = user_activation_token.make_token(user)
    url_change_password = f'/users/user_change_password/{uid}/{token}/'
    payload = {
        'password': 'Othed@##Passw0RD!',
        'confirm_password': 'Othed@##Passw0RD!' ,
    }
    response_change_password = create_user_and_login_payload.post(url_change_password, payload, format='json')
    user.refresh_from_db()
    new_password = user.password
    assert old_password != new_password
    assert response_change_password.status_code == 200


@pytest.mark.django_db
def test_create_message(create_user_and_login_payload):
    # Test POST request to send message to tehnical
    # support.
    url = f'/users/message_create_or_list/'
    payload = {
        'message_text': fake.text(),
    }
    response = create_user_and_login_payload.post(url, payload, response='json')
    assert response.status_code == 201


@pytest.mark.django_db
def test_list_of_messages(create_user_and_login_payload):
    # Test GET request for receiving all messages
    # which have been sent by and to user.
    url = f'/users/message_create_or_list/'
    payload_first_message = {
        'message_text': fake.text(),
    }
    response = create_user_and_login_payload.post(url, payload_first_message, response='json')
    payload_senond_message = {
        'message_text': fake.text(),
    }
    response = create_user_and_login_payload.post(url, payload_senond_message, response='json')

    response = create_user_and_login_payload.get(url)

    assert Message.objects.count() == 4
    assert response.status_code == 200




@pytest.mark.django_db
def test_create_notary_by_admin(create_user_and_login_payload):
    url = f'/users/notary/'
    payload_notary = {
        'name': fake.name(),
        'surname': fake.name(),
        'phone': fake.phone_number(),
        'email': fake.email(),
    }
    response = create_user_and_login_payload.post(url, payload_notary, response='json')
    assert response.status_code == 201


# @pytest.mark.django_db
# def test_update_notary_by_admin(create_admin_payload):
#     url = f'/users/notary/'
#     payload_notary = {
#         'name': fake.name(),
#         'surname': fake.name(),
#         'phone': fake.phone_number(),
#         'email': fake.email(),
#     }
#     create_admin_payload.post(url, payload_notary, response='json')
#     notary = Notary.objects.first()
#     url = f'/users/notary/{notary.id}/'
#     response = create_admin_payload.post(url, payload_notary, response='json')
#     payload_put_notary = {
#         'name': fake.name(),
#         'surname': fake.name(),
#         'phone': fake.phone_number(),
#         'email': fake.email(),
#     }
#     response_put_update = create_admin_payload.put(url, payload_put_notary, response='json')
#     assert response_put_update.status_code == 200

#     payload_patch_notary = {
#         'name': fake.name(),
#         'surname': fake.name(),
#         'phone': fake.phone_number(),
#         'email': fake.email(),
#     }
#     response_patch_update = create_admin_payload.patch(url, payload_patch_notary, response='json')
#     assert response_patch_update.status_code == 200



# @pytest.mark.django_db
# def test_delete_notary_by_admin(create_admin_payload):
#     url = f'/users/notary/'
#     payload_notary = {
#         'name': fake.name(),
#         'surname': fake.name(),
#         'phone': fake.phone_number(),
#         'email': fake.email(),
#     }
#     create_admin_payload.post(url, payload_notary, response='json')
#     notary = Notary.objects.first()
#     url = f'/users/notary/{notary.id}/'
#     response_delete = create_admin_payload.delete(url)
#     assert response_delete.status_code == 204


@pytest.mark.django_db
def test_retreave_notary_by_simpe_user(create_user_and_login_payload):

    payload_notary = {
        'name': fake.name(),
        'surname': fake.name(),
        'phone': fake.phone_number(),
        'email': fake.email(),
    }
    notary = Notary.objects.create(name=fake.name(),
                                    surname=fake.name(),
                                    phone=fake.phone_number(),
                                    email=fake.email())
    url = f'/users/notary/{notary.id}/'
    response = create_user_and_login_payload.get(url)
    assert response.status_code == 200



@pytest.mark.django_db
def test_retreave_list_notary_by_simple_user(create_user_and_login_payload):

    for i in range (1, 3):
        notary = Notary.objects.create(name=fake.name(),
                                        surname=fake.name(),
                                        phone=fake.phone_number(),
                                        email=fake.email())
    url = f'/users/notary/'
    response = create_user_and_login_payload.get(url)
    assert response.status_code == 200
    assert Notary.objects.count() == 2
# # ================================END=TESTS====================================