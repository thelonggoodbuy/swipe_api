import pytest
from users.models import CustomUser
from houses.models import House, HouseEntrance



@pytest.mark.django_db
def test_house_entrance_partly_update(generate_house_fixture_with_subordinate_objects_fixture,
                                 create_builder_user_and_authenticate_fixture):
    house = House.objects.get(description = "description_test_1")
    builder = CustomUser.objects.get(email='test_builder_123@mail.com')
    house.builder = builder
    house.save()
    entrance = house.house_entrance.first()
    payload = {'house': house.id, 'title': 'Changed Entrance'}
    url = f'/houses/house_entrance/{entrance.id}/'
    response = create_builder_user_and_authenticate_fixture.patch(url, payload, response='json')
    entrance = house.house_entrance.first()
    assert entrance.title == 'Changed Entrance'
    assert response.status_code == 200