import pytest
from users.models import CustomUser


@pytest.mark.django_db
def test_user_detail(create_user_and_authenticate_fixture):
    user = CustomUser.objects.get(email='test123_email@mail.com')
    url = f'/users/simple_user_update_and_detail/{user.id}/'
    response = create_user_and_authenticate_fixture.get(url, format='json')
    assert response.status_code == 200