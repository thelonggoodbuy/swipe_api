import pytest
from users.models import CustomUser
from django.utils.encoding import force_bytes
from faker import Faker
from users.tokens import user_activation_token
from django.utils.http import urlsafe_base64_encode


fake = Faker()


@pytest.mark.django_db
def test_change_password(create_user_and_authenticate_fixture):
    # Test POST request to change password throw
    # token (in users app this token is used for
    # email change password confirmation)
    user = CustomUser.objects.get(email="test123_email@mail.com")
    old_password = user.password
    url = f'/users/user_change_password_request/{user.id}/'
    create_user_and_authenticate_fixture.get(url)
    uid = urlsafe_base64_encode(force_bytes(user.id))
    token = user_activation_token.make_token(user)
    url_change_password = f'/users/user_change_password/{uid}/{token}/'
    payload = {
        'password': 'Othed@##Passw0RD!',
        'confirm_password': 'Othed@##Passw0RD!' ,
    }
    response_change_password = create_user_and_authenticate_fixture.post(url_change_password, payload, format='json')
    user.refresh_from_db()
    new_password = user.password
    assert old_password != new_password
    assert response_change_password.status_code == 200