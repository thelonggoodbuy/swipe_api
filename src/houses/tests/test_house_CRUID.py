import pytest
from users.models import CustomUser
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from users.tokens import user_activation_token

from houses.models import House, HouseEntrance, Floor, Riser, HouseBuilding



@pytest.mark.django_db
def test_simple_user_activation_registration(api_client_fixture):
    # Testing email confirmation with creation simple user.
    url = '/users/auth/register_simple_user/'
    payload = {
        "email": "test_user@gmail.com",
        "password": "test_password_123!@",
        "is_simple_user": True,
    }
    response = api_client_fixture.post(url, payload, response='json')
    user = CustomUser.objects.get(email='test_user@gmail.com')
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = user_activation_token.make_token(user)
    activation_url = f'/users/auth/activate_simple_user/{uid}/{token}/'
    response_for_activation = api_client_fixture.get(activation_url)
    user.refresh_from_db()
    assert user.is_activated == True
    assert response_for_activation.status_code == 200



@pytest.mark.django_db
def test_create_house(generate_data_for_creating_house_fixture):
    url = f'/houses/houses/'
    payload = generate_data_for_creating_house_fixture.data['house_payload']
    response = generate_data_for_creating_house_fixture.post(url, payload, response='json')
    assert response.status_code == 201



@pytest.mark.django_db
def test_update_house(create_builder_user_and_authenticate_fixture,\
                      generate_house_fixture):
    house = House.objects.get(description = "description_test_1")
    builder = CustomUser.objects.get(email='test_builder_123@mail.com')
    house.builder = builder
    house.save()
    url = f'/houses/houses/{house.id}/'
    payload = {"address": "address_test_2"}
    response = create_builder_user_and_authenticate_fixture.patch(url, payload, response='json')
    assert response.status_code == 200
    payload = {"address": "address_test_3"}
    response = create_builder_user_and_authenticate_fixture.put(url, payload, response='json')
    assert response.status_code == 200


@pytest.mark.django_db
def test_retreave_house(create_builder_user_and_authenticate_fixture,\
                      generate_house_fixture):
    house = House.objects.get(description = "description_test_1")
    builder = CustomUser.objects.get(email='test_builder_123@mail.com')
    house.builder = builder
    house.save()
    url = f'/houses/houses/{house.id}/'
    response = create_builder_user_and_authenticate_fixture.get(url, response='json')
    assert response.status_code == 200


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


@pytest.mark.django_db
def test_list_house(generate_multiple_house_fixture,\
                    create_builder_user_and_authenticate_fixture):
    
    builder = CustomUser.objects.get(email='test_builder_123@mail.com')
    for house in House.objects.filter(description='description_test_1'):
        house.builder = builder
        house.save()
    houses_list = House.objects.filter(builder=builder)
    assert houses_list.count() == 2
    url = f'/houses/houses/'
    response = create_builder_user_and_authenticate_fixture.get(url, response='json')
    assert response.status_code == 200



# ----------------------------------------------------------------------------------
# -------------------ENTRANCES-------TEST-------------------------------------------
# ----------------------------------------------------------------------------------


@pytest.mark.django_db
def test_house_entrance_retreave(generate_house_fixture_with_subordinate_objects_fixture,
                                 create_builder_user_and_authenticate_fixture):
    house = House.objects.get(description = "description_test_1")
    builder = CustomUser.objects.get(email='test_builder_123@mail.com')
    house.builder = builder
    house.save()
    house_entrance = HouseEntrance.objects.get(title='first_entrance')
    url = f'/houses/house_entrance/{house_entrance.id}/'
    response = create_builder_user_and_authenticate_fixture.get(url, response='json')
    assert response.status_code == 200


@pytest.mark.django_db
def test_house_entrance_list(generate_house_fixture_with_subordinate_objects_fixture,
                                 create_builder_user_and_authenticate_fixture):
    house = House.objects.get(description = "description_test_1")
    builder = CustomUser.objects.get(email='test_builder_123@mail.com')
    house.builder = builder
    house.save()
    house_entrances_quantity = HouseEntrance.objects.filter(house=house).count()
    url = f'/houses/house_entrance/'
    response = create_builder_user_and_authenticate_fixture.get(url, response='json')
    assert response.status_code == 200
    assert house_entrances_quantity == 2


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


@pytest.mark.django_db
def test_house_entrance_update(generate_house_fixture_with_subordinate_objects_fixture,
                                 create_builder_user_and_authenticate_fixture):
    house = House.objects.get(description = "description_test_1")
    builder = CustomUser.objects.get(email='test_builder_123@mail.com')
    house.builder = builder
    house.save()
    entrance = house.house_entrance.first()
    payload = {'house': house.id, 'title': 'Changed Entrance'}
    url = f'/houses/house_entrance/{entrance.id}/'
    response = create_builder_user_and_authenticate_fixture.put(url, payload, response='json')
    entrance = house.house_entrance.first()
    assert entrance.title == 'Changed Entrance'
    assert response.status_code == 200


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




# ----------------------------------------------------------------------------------
# -------------------FLOORS-------TEST----------------------------------------------
# ----------------------------------------------------------------------------------
@pytest.mark.django_db
def test_house_floor_retreave(generate_house_fixture_with_subordinate_objects_fixture,
                                 create_builder_user_and_authenticate_fixture):
    house = House.objects.get(description = "description_test_1")
    builder = CustomUser.objects.get(email='test_builder_123@mail.com')
    house.builder = builder
    house.save()
    house_floor = Floor.objects.get(title='first_floor')
    url = f'/houses/house_floor/{house_floor.id}/'
    response = create_builder_user_and_authenticate_fixture.get(url, response='json')
    assert response.status_code == 200


@pytest.mark.django_db
def test_house_floor_list(generate_house_fixture_with_subordinate_objects_fixture,
                                 create_builder_user_and_authenticate_fixture):
    house = House.objects.get(description = "description_test_1")
    builder = CustomUser.objects.get(email='test_builder_123@mail.com')
    house.builder = builder
    house.save()
    house_floor_quantity = Floor.objects.filter(house=house).count()
    url = f'/houses/house_floor/'
    response = create_builder_user_and_authenticate_fixture.get(url, response='json')
    assert response.status_code == 200
    assert house_floor_quantity == 2


@pytest.mark.django_db
def test_house_floor_create(generate_house_fixture_with_subordinate_objects_fixture,
                                 create_builder_user_and_authenticate_fixture):
    house = House.objects.get(description = "description_test_1")
    builder = CustomUser.objects.get(email='test_builder_123@mail.com')
    house.builder = builder
    house.save()

    payload = {'house': house.id, 'title': 'third_house_floor'}
    url = f'/houses/house_floor/'
    response = create_builder_user_and_authenticate_fixture.post(url, payload, response='json')
    house_floors_quantity = Floor.objects.filter(house=house).count()
    assert response.status_code == 201
    assert house_floors_quantity == 3


@pytest.mark.django_db
def test_house_floors_update(generate_house_fixture_with_subordinate_objects_fixture,
                                 create_builder_user_and_authenticate_fixture):
    house = House.objects.get(description = "description_test_1")
    builder = CustomUser.objects.get(email='test_builder_123@mail.com')
    house.builder = builder
    house.save()
    floor = house.floor.first()
    payload = {'house': house.id, 'title': 'Changed Floor'}
    url = f'/houses/house_floor/{floor.id}/'
    response = create_builder_user_and_authenticate_fixture.put(url, payload, response='json')
    entrance = house.floor.first()
    assert entrance.title == 'Changed Floor'
    assert response.status_code == 200


@pytest.mark.django_db
def test_house_floors_partly_update(generate_house_fixture_with_subordinate_objects_fixture,
                                 create_builder_user_and_authenticate_fixture):
    house = House.objects.get(description = "description_test_1")
    builder = CustomUser.objects.get(email='test_builder_123@mail.com')
    house.builder = builder
    house.save()
    floor = house.floor.first()
    payload = {'house': house.id, 'title': 'Changed Floor'}
    url = f'/houses/house_floor/{floor.id}/'
    response = create_builder_user_and_authenticate_fixture.patch(url, payload, response='json')
    entrance = house.floor.first()
    assert entrance.title == 'Changed Floor'
    assert response.status_code == 200


@pytest.mark.django_db
def test_house_floor_delete(generate_house_fixture_with_subordinate_objects_fixture,
                                 create_builder_user_and_authenticate_fixture):
    house = House.objects.get(description = "description_test_1")
    builder = CustomUser.objects.get(email='test_builder_123@mail.com')
    house.builder = builder
    house.save()
    floor = house.floor.first()
    url = f'/houses/house_floor/{floor.id}/'
    response = create_builder_user_and_authenticate_fixture.delete(url, response='json')
    assert response.status_code == 204

# ----------------------------------------------------------------------------------
# -------------------HOUSE-----BUILDING-------TEST----------------------------------
# ----------------------------------------------------------------------------------

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


@pytest.mark.django_db
def test_house_building_list(generate_house_fixture_with_subordinate_objects_fixture,
                                 create_builder_user_and_authenticate_fixture):
    house = House.objects.get(description = "description_test_1")
    builder = CustomUser.objects.get(email='test_builder_123@mail.com')
    house.builder = builder
    house.save()
    house_house_building_quantity = HouseBuilding.objects.filter(house=house).count()
    url = f'/houses/houses_building/'
    response = create_builder_user_and_authenticate_fixture.get(url, response='json')
    assert response.status_code == 200
    assert house_house_building_quantity == 2


@pytest.mark.django_db
def test_house_house_building_create(generate_house_fixture_with_subordinate_objects_fixture,
                                 create_builder_user_and_authenticate_fixture):
    house = House.objects.get(description = "description_test_1")
    builder = CustomUser.objects.get(email='test_builder_123@mail.com')
    house.builder = builder
    house.save()

    payload = {'house': house.id, 'title': 'third_house_building'}
    url = f'/houses/houses_building/'
    response = create_builder_user_and_authenticate_fixture.post(url, payload, response='json')
    house_floors_quantity = HouseBuilding.objects.filter(house=house).count()
    assert response.status_code == 201
    assert house_floors_quantity == 3


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


@pytest.mark.django_db
def test_house_building_partly_update(generate_house_fixture_with_subordinate_objects_fixture,
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


@pytest.mark.django_db
def test_house_building_delete(generate_house_fixture_with_subordinate_objects_fixture,
                                 create_builder_user_and_authenticate_fixture):
    house = House.objects.get(description = "description_test_1")
    builder = CustomUser.objects.get(email='test_builder_123@mail.com')
    house.builder = builder
    house.save()

    house_building = house.house_building.first()
    url = f'/houses/houses_building/{house_building.id}/'
    response = create_builder_user_and_authenticate_fixture.delete(url, response='json')
    assert response.status_code == 204



# ----------------------------------------------------------------------------------
# ----------------------RISERS-------TEST-------------------------------------------
# ----------------------------------------------------------------------------------

@pytest.mark.django_db
def test_house_riser_retreave(generate_house_fixture_with_subordinate_objects_fixture,
                                 create_builder_user_and_authenticate_fixture):
    house = House.objects.get(description = "description_test_1")
    builder = CustomUser.objects.get(email='test_builder_123@mail.com')
    house.builder = builder
    house.save()
    house_riser = Riser.objects.get(title='first_house_riser')
    url = f'/houses/house_riser/{house_riser.id}/'
    response = create_builder_user_and_authenticate_fixture.get(url, response='json')
    assert response.status_code == 200


@pytest.mark.django_db
def test_house_riser_list(generate_house_fixture_with_subordinate_objects_fixture,
                                 create_builder_user_and_authenticate_fixture):
    house = House.objects.get(description = "description_test_1")
    builder = CustomUser.objects.get(email='test_builder_123@mail.com')
    house.builder = builder
    house.save()

    riser_quantity = Riser.objects.filter(house=house).count()
    url = f'/houses/house_riser/'
    response = create_builder_user_and_authenticate_fixture.get(url, response='json')
    assert response.status_code == 200
    assert riser_quantity == 2


@pytest.mark.django_db
def test_house_riser_create(generate_house_fixture_with_subordinate_objects_fixture,
                                 create_builder_user_and_authenticate_fixture):
    house = House.objects.get(description = "description_test_1")
    builder = CustomUser.objects.get(email='test_builder_123@mail.com')
    house.builder = builder
    house.save()

    payload = {'house': house.id, 'title': 'third_house_riser'}
    url = f'/houses/house_riser/'
    response = create_builder_user_and_authenticate_fixture.post(url, payload, response='json')
    house_risers_quantity = Riser.objects.filter(house=house).count()
    assert response.status_code == 201
    assert house_risers_quantity == 3


@pytest.mark.django_db
def test_house_riser_update(generate_house_fixture_with_subordinate_objects_fixture,
                                 create_builder_user_and_authenticate_fixture):
    house = House.objects.get(description = "description_test_1")
    builder = CustomUser.objects.get(email='test_builder_123@mail.com')
    house.builder = builder
    house.save()
    house_riser = house.riser.first()
    payload = {'house': house.id, 'title': 'Changed smth in risers'}
    url = f'/houses/house_riser/{house_riser.id}/'
    response = create_builder_user_and_authenticate_fixture.put(url, payload, response='json')
    house_riser = house.riser.first()
    assert house_riser.title == 'Changed smth in risers'
    assert response.status_code == 200


@pytest.mark.django_db
def test_house_riser_partly_update(generate_house_fixture_with_subordinate_objects_fixture,
                                 create_builder_user_and_authenticate_fixture):
    house = House.objects.get(description = "description_test_1")
    builder = CustomUser.objects.get(email='test_builder_123@mail.com')
    house.builder = builder
    house.save()
    house_riser = house.riser.first()
    payload = {'house': house.id, 'title': 'Changed smth new in risers'}
    url = f'/houses/house_riser/{house_riser.id}/'
    response = create_builder_user_and_authenticate_fixture.put(url, payload, response='json')
    house_riser = house.riser.first()
    assert house_riser.title == 'Changed smth new in risers'
    assert response.status_code == 200


@pytest.mark.django_db
def test_house_riser_delete(generate_house_fixture_with_subordinate_objects_fixture,
                                 create_builder_user_and_authenticate_fixture):
    house = House.objects.get(description = "description_test_1")
    builder = CustomUser.objects.get(email='test_builder_123@mail.com')
    house.builder = builder
    house.save()

    house_riser = house.riser.first()
    url = f'/houses/house_riser/{house_riser.id}/'
    response = create_builder_user_and_authenticate_fixture.delete(url, response='json')
    assert response.status_code == 204

