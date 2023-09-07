import pytest
from users.models import CustomUser
from houses.models import House, HouseEntrance


@pytest.mark.django_db
def test_house_entrance_create(generate_house_fixture_with_subordinate_objects_fixture,
                                 create_builder_user_and_authenticate_fixture):
    house = House.objects.get(description = "description_test_1")
    builder = CustomUser.objects.get(email='test_builder_123@mail.com')
    house.builder = builder
    house.save()

    payload = {'house': house.id, 'title': 'third_house_entrance'}
    url = f'/houses/house_entrance/'
    response = create_builder_user_and_authenticate_fixture.post(url, payload, response='json')
    house_entrances_quantity = HouseEntrance.objects.filter(house=house).count()
    assert response.status_code == 201
    assert house_entrances_quantity == 3