import pytest
from users.models import CustomUser
from houses.models import House
from ads.models import Accomodation
from pathlib import Path
import base64
import json



@pytest.mark.django_db
def test_patch_string_data_and_create_images_accomodation(generate_multiple_accomodations_fixture,\
                            create_builder_user_and_authenticate_fixture):
    
    builder = CustomUser.objects.get(email='test_builder_123@mail.com')
    house = House.objects.get(description = "description_test_1")
    house.builder = builder
    house.save()
    needfull_accomodation = Accomodation.objects.get(number=1, house=house)

    url = f'/ads/accomodation/{needfull_accomodation.id}/'
    payload = {
        'number': 10,
        'image_field': []
    }

    p = Path(__file__).parent
    fileaddress = p.joinpath('test_data', 'test_image_4.jpg')
    with open(fileaddress, 'rb') as image_file:
        third_image_base64_bytes = base64.b64encode(image_file.read())
        third_image_base64_string = third_image_base64_bytes.decode()
        third_image_dict = {
            "obj_order": 3,
            "image": third_image_base64_string
        }
        payload['image_field'].append(third_image_dict)

    fileaddress = p.joinpath('test_data', 'test_image_5.jpg')
    with open(fileaddress, 'rb') as image_file:
        fourth_image_base64_bytes = base64.b64encode(image_file.read())
        fourth_image_base64_string = fourth_image_base64_bytes.decode()
        fourth_image_dict = {
            "obj_order": 5,
            "image": fourth_image_base64_string
        }
        payload['image_field'].append(fourth_image_dict)


    payload = json.dumps(payload, indent=4)

    response = create_builder_user_and_authenticate_fixture\
                .patch(url, payload, content_type="application/json", response='json')

    needfull_accomodation.refresh_from_db()
    needfull_accomodation = Accomodation.objects.get(number=10, house=house)

    assert response.status_code == 200
    assert needfull_accomodation.number == 10
    assert needfull_accomodation.image_field.all().count() == 4


@pytest.mark.django_db
def test_patch_string_data_and_delete_images_accomodation(generate_multiple_accomodations_fixture,\
                            create_builder_user_and_authenticate_fixture):
    
    builder = CustomUser.objects.get(email='test_builder_123@mail.com')
    house = House.objects.get(description = "description_test_1")
    house.builder = builder
    house.save()
    needfull_accomodation = Accomodation.objects.get(number=1, house=house)

    deletable_image = needfull_accomodation.image_field.all().first()

    url = f'/ads/accomodation/{needfull_accomodation.id}/'
    payload = {
        'number': 10,
        'image_field': [{"id": deletable_image.id}]
    }

    payload = json.dumps(payload, indent=4)
    response = create_builder_user_and_authenticate_fixture\
                .patch(url, payload, content_type="application/json",\
                        response='json')

    needfull_accomodation.refresh_from_db()
    assert response.status_code == 200
    assert needfull_accomodation.image_field.all().count() == 1


@pytest.mark.django_db
def test_patch_string_data_and_change_order_images_accomodation(generate_multiple_accomodations_fixture,\
                            create_builder_user_and_authenticate_fixture):
    
    builder = CustomUser.objects.get(email='test_builder_123@mail.com')
    house = House.objects.get(description = "description_test_1")
    house.builder = builder
    house.save()
    needfull_accomodation = Accomodation.objects.get(number=1, house=house)

    first_image = needfull_accomodation.image_field.all().first()
    second_image = needfull_accomodation.image_field.all().last()

    old_first_image_order = first_image.obj_order
    old_second_image_order = second_image.obj_order

    url = f'/ads/accomodation/{needfull_accomodation.id}/'
    payload = {
        'number': 10,
        'image_field': [{"id": first_image.id, "obj_order": second_image.obj_order},
                        {"id": second_image.id, "obj_order": first_image.obj_order}]
    }

    payload = json.dumps(payload, indent=4)
    response = create_builder_user_and_authenticate_fixture\
                .patch(url, payload, content_type="application/json",\
                        response='json')

    needfull_accomodation.refresh_from_db()
    assert response.status_code == 200
    assert needfull_accomodation.image_field.all().count() == 2
    assert needfull_accomodation.image_field.first().obj_order == old_second_image_order
    assert needfull_accomodation.image_field.last().obj_order == old_first_image_order


@pytest.mark.django_db
def test_patch_string_data_and_change_images_accomodation(generate_multiple_accomodations_fixture,\
                            create_builder_user_and_authenticate_fixture):
    
    builder = CustomUser.objects.get(email='test_builder_123@mail.com')
    house = House.objects.get(description = "description_test_1")
    house.builder = builder
    house.save()
    needfull_accomodation = Accomodation.objects.get(number=1, house=house)

    first_image = needfull_accomodation.image_field.first()
    old_image = first_image.image

    url = f'/ads/accomodation/{needfull_accomodation.id}/'
    payload = {
        'number': 10,
        'image_field': []
    }

    p = Path(__file__).parent
    fileaddress = p.joinpath('test_data', 'test_image_4.jpg')
    with open(fileaddress, 'rb') as image_file:
        updated_image_base64_bytes = base64.b64encode(image_file.read())
        updated_image_base64_string = updated_image_base64_bytes.decode()
        changed_dict = {
            "id": first_image.id,
            "obj_order": first_image.obj_order,
            "image": updated_image_base64_string
        }
        payload['image_field'].append(changed_dict)

    payload = json.dumps(payload, indent=4)

    response = create_builder_user_and_authenticate_fixture\
                .patch(url, payload, content_type="application/json", response='json')

    needfull_accomodation.refresh_from_db()
    needfull_accomodation = Accomodation.objects.get(number=10, house=house)

    new_image = needfull_accomodation.image_field.first().image

    assert old_image != new_image
    assert response.status_code == 200
    assert needfull_accomodation.number == 10
    assert needfull_accomodation.image_field.all().count() == 2
