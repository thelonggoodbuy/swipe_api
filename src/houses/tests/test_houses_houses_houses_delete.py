
import pytest
from users.models import CustomUser
from houses.models import House


@pytest.mark.django_db
def test_delete_house(create_builder_user_and_authenticate_fixture,\
                      generate_house_fixture):
    house = House.objects.get(description = "description_test_1")
    builder = CustomUser.objects.get(email='test_builder_123@mail.com')
    house.builder = builder
    house.save()
    url = f'/houses/houses/{house.id}/'
    response = create_builder_user_and_authenticate_fixture.delete(url)
    assert response.status_code == 204