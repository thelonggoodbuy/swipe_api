import pytest
from rest_framework import status
from users.models import CustomUser





@pytest.mark.django_db
def test_simple_user_registration(api_client_fixture, db):
    # Testing creating a simple user entrypoint
    # without email confirmation.
    url = '/users/auth/register_simple_user/'
    payload = {
        "email": "test_user@gmail.com",
        "password": "test_password_123!@",
        "is_simple_user": True,
    }
    response = api_client_fixture.post(url, payload, response='json')
    assert response.status_code == status.HTTP_201_CREATED