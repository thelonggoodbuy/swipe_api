import pytest
from users.models import CustomUser
from houses.models import House, HouseEntrance



@pytest.mark.django_db
def test_house_entrance_delete(generate_house_fixture_with_subordinate_objects_fixture,
                                 create_builder_user_and_authenticate_fixture):
    house = House.objects.get(description = "description_test_1")
    builder = CustomUser.objects.get(email='test_builder_123@mail.com')
    house.builder = builder
    house.save()
    entrance = house.house_entrance.first()
    url = f'/houses/house_entrance/{entrance.id}/'
    response = create_builder_user_and_authenticate_fixture.delete(url, response='json')
    assert response.status_code == 204