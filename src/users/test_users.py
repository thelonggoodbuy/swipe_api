import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.conf import settings
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from faker import Faker
from rest_framework_simplejwt.tokens import RefreshToken

from .models import CustomUser
from .tokens import user_activation_token

fake = Faker()


# ========================================FIXTURE==============================
@pytest.fixture
def api_client():
    client = APIClient()
    return client


@pytest.fixture
def create_user_payload():
    payload = {
        "email": "test_user@gmail.com",
        "is_simple_user": True
    }
    test_user = CustomUser(**payload)
    test_user.set_password("test_password_123!@")
    test_user.save()
    return test_user

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

# ====================================END=FIXTURE==============================

# ====================================TESTS====================================

@pytest.mark.django_db
def test_simple_user_registration(api_client):
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


@pytest.mark.django_db
def test_get_simple_user_data(create_user_and_login_payload):
    # Test retreave(GET) simple user entrypoint.

    user = CustomUser.objects.get(email="test_loggined_user@gmail.com")
    url = f'/users/simple_user_update_and_detail/{user.id}/'
    response = create_user_and_login_payload.get(url, format='json')
    assert response.status_code == 200


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
    payload = {
        'message_text': fake.text(),
    }
    response = create_user_and_login_payload.post(url, payload, response='json')

    url = f'/users/message_create_or_list/'
    response = create_user_and_login_payload.get(url)

    assert response.status_code == 200

# ================================END=TESTS====================================