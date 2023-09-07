import pytest
from users.models import CustomUser
from houses.models import House, HouseBuilding


@pytest.mark.django_db
def test_house_building_retreave(generate_house_fixture_with_subordinate_objects_fixture,
                                 create_builder_user_and_authenticate_fixture):
    house = House.objects.get(description = "description_test_1")
    builder = CustomUser.objects.get(email='test_builder_123@mail.com')
    house.builder = builder
    house.save()
    house_building = HouseBuilding.objects.get(title='first_house_building')
    url = f'/houses/houses_building/{house_building.id}/'
    response = create_builder_user_and_authenticate_fixture.get(url, response='json')
    assert response.status_code == 200