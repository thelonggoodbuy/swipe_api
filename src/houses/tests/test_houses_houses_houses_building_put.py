import pytest
from users.models import CustomUser
from houses.models import House, HouseBuilding





@pytest.mark.django_db
def test_house_building_update(generate_house_fixture_with_subordinate_objects_fixture,
                                 create_builder_user_and_authenticate_fixture):
    house = House.objects.get(description = "description_test_1")
    builder = CustomUser.objects.get(email='test_builder_123@mail.com')
    house.builder = builder
    house.save()

    house_building = house.house_building.first()
    payload = {'house': house.id, 'title': 'Changed house building'}
    url = f'/houses/houses_building/{house_building.id}/'
    response = create_builder_user_and_authenticate_fixture.put(url, payload, response='json')
    house_building = house.house_building.first()
    assert house_building.title == 'Changed house building'
    assert response.status_code == 200