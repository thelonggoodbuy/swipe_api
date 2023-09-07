import pytest
from users.models import CustomUser
from houses.models import House
from ads.models import Accomodation
from pathlib import Path
import base64
import json




@pytest.mark.django_db
def test_put_accomodation(generate_multiple_accomodations_fixture,\
                            create_builder_user_and_authenticate_fixture):
    
    builder = CustomUser.objects.get(email='test_builder_123@mail.com')
    house = House.objects.get(description = "description_test_1")
    house.builder = builder
    house.save()
    needfull_accomodation = Accomodation.objects.get(number=1, house=house)
    url = f'/ads/accomodation/{needfull_accomodation.id}/'
    payload = {
        "number": 10,
        "type_status": "new_building",
        "area": 100,
        "planing": "two_bedroom_and_roof",
        "living_condition": "reary_for_settlement",
        "area_kitchen": 43,
        "heat_type": "electric",
        "have_balcony": True,
        "image_field": []
    }

    p = Path(__file__).parents[3]
    fileaddress = p.joinpath('seed/test_data/images', 'test_image_2.jpg')
    with open(fileaddress, 'rb') as image_file:
        second_image_base64_bytes = base64.b64encode(image_file.read())
        second_image_base64_string = second_image_base64_bytes.decode()
        second_image_dict = {
            "obj_order": 3,
            "image": second_image_base64_string
        }
        payload['image_field'].append(second_image_dict)

    payload = json.dumps(payload, indent=4)

    response = create_builder_user_and_authenticate_fixture.put(url, payload, content_type="application/json",  response='json')
    needfull_accomodation.refresh_from_db()
    needfull_accomodation.number == 10

    assert response.status_code == 200
    assert needfull_accomodation.type_status == "new_building"
    assert needfull_accomodation.area == 100
    assert needfull_accomodation.planing == "two_bedroom_and_roof"
    assert needfull_accomodation.living_condition == 'reary_for_settlement'
    assert needfull_accomodation.area_kitchen == 43
    assert needfull_accomodation.heat_type == 'electric'

