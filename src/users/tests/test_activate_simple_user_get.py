import pytest
from users.models import CustomUser
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from users.tokens import user_activation_token




@pytest.mark.django_db
def test_simple_user_activation_registration(api_client_fixture):
    # Testing email confirmation with creation simple user.
    url = '/users/auth/register_simple_user/'
    payload = {
        "email": "test_user@gmail.com",
        "password": "test_password_123!@",
        "is_simple_user": True,
    }
    response = api_client_fixture.post(url, payload, response='json')
    user = CustomUser.objects.get(email='test_user@gmail.com')
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = user_activation_token.make_token(user)
    activation_url = f'/users/auth/activate_simple_user/{uid}/{token}/'
    response_for_activation = api_client_fixture.get(activation_url)
    user.refresh_from_db()
    assert user.is_activated == True
    assert response_for_activation.status_code == 200