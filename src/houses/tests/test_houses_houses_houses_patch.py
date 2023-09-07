
import pytest
from users.models import CustomUser
from houses.models import House

@pytest.mark.django_db
def test_update_house(create_builder_user_and_authenticate_fixture,\
                      generate_house_fixture):
    house = House.objects.get(description = "description_test_1")
    builder = CustomUser.objects.get(email='test_builder_123@mail.com')
    house.builder = builder
    house.save()
    url = f'/houses/houses/{house.id}/'
    payload = {"address": "address_test_2"}

    old_address = house.address
    response = create_builder_user_and_authenticate_fixture.patch(url, payload, response='json')

    house.refresh_from_db()
    new_address = house.address

    assert response.status_code == 200
    assert old_address != new_address