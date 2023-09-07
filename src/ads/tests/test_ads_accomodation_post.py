import pytest
from users.models import CustomUser
from houses.models import House


from pathlib import Path
import base64



@pytest.mark.django_db
def test_create_accomodation(generate_house_fixture_with_subordinate_objects_fixture,\
                            create_builder_user_and_authenticate_fixture):
    builder = CustomUser.objects.get(email='test_builder_123@mail.com')
    house = House.objects.get(description = "description_test_1")
    house.builder = builder
    house.save()

    url = f'/ads/accomodation/'

    payload = {
        'type_status': 'new_building',
        'number': 1,
        'house': house.id,
        'house_building': house.house_building.first().id,
        'house_entrance': house.house_entrance.first().id,
        'floor': house.floor.first().id,
        'riser': house.riser.first().id,
        'area': 65,
        'planing': 'two_bedroom',
        'living_condition': 'need_repair',
        'area_kitchen': 18,
        'have_balcony': True,
        'heat_type': 'electric',
        'image_field': [],
        'is_shown_in_chesboard': False
    }
    
    p = Path(__file__).parent

    fileaddress = p.joinpath('test_data', 'test_image_1.jpg')
    image_file = open(fileaddress, 'rb')
    with open(fileaddress, 'rb') as image_file:
        image_base64_bytes = base64.b64encode(image_file.read())
        image_base64_string = image_base64_bytes.decode()
        payload['schema'] = image_base64_string

    fileaddress = p.joinpath('test_data', 'test_image_2.jpg')
    with open(fileaddress, 'rb') as image_file:
        first_image_base64_bytes = base64.b64encode(image_file.read())
        first_image_base64_string = first_image_base64_bytes.decode()
        first_image_dict = {
            "obj_order": 0,
            "image": first_image_base64_string
        }
        payload['image_field'].append(first_image_dict)

    fileaddress = p.joinpath('test_data', 'test_image_3.jpg')
    with open(fileaddress, 'rb') as image_file:
        second_image_base64_bytes = base64.b64encode(image_file.read())
        second_image_base64_string = second_image_base64_bytes.decode()
        second_image_dict = {
            "obj_order": 1,
            "image": second_image_base64_string
        }
        payload['image_field'].append(second_image_dict)

    url = f'/ads/accomodation/'
    response = create_builder_user_and_authenticate_fixture.post(url, payload, format='json', response='json')

    assert response.status_code == 201
    assert house.accomodation.all().count() == 1