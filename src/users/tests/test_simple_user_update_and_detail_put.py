import pytest
from users.models import CustomUser

from faker import Faker

fake = Faker()

@pytest.mark.django_db
def test_put_simple_user_data(create_user_and_authenticate_fixture):
    # Test updating(PUT) simple user entrypoint.

    payload = {
        'first_name': fake.name(),
        'second_name': fake.name()
    }
    user = CustomUser.objects.get(email="test123_email@mail.com")
    url = f'/users/simple_user_update_and_detail/{user.id}/'
    response = create_user_and_authenticate_fixture.put(url, payload, format='json')
    user.refresh_from_db()
    assert user.first_name == payload['first_name']
    assert user.second_name == payload['second_name']
    assert user.email == 'test123_email@mail.com'
    assert response.status_code == 200