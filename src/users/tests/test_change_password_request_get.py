import pytest
from users.models import CustomUser





@pytest.mark.django_db
def test_change_password_request(create_user_and_authenticate_fixture):
    # Test GET request for changing password
    user = CustomUser.objects.get(email="test123_email@mail.com")
    url = f'/users/user_change_password_request/{user.id}/'
    response = create_user_and_authenticate_fixture.get(url)
    assert response.status_code == 201