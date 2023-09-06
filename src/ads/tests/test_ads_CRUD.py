import pytest
from users.models import CustomUser
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from users.tokens import user_activation_token

from houses.models import House
from ads.models import Filter

from pathlib import Path
from django.core.files.uploadedfile import SimpleUploadedFile
from ads.models import ImageGalery
import base64

from ads.models import Accomodation, Ads, PromoAdditionalPhrase

from decimal import Decimal
import json


@pytest.mark.django_db
def test_list_accomodation(generate_multiple_accomodations_fixture,\
                            create_builder_user_and_authenticate_fixture):
    
    builder = CustomUser.objects.get(email='test_builder_123@mail.com')
    house = House.objects.get(description = "description_test_1")
    house.builder = builder
    house.save()

    url = f'/ads/accomodation/'
    response = create_builder_user_and_authenticate_fixture.get(url, response='json')
    assert response.status_code == 200


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


@pytest.mark.django_db
def test_retreave_accomodation(generate_multiple_accomodations_fixture,\
                            create_builder_user_and_authenticate_fixture):
    
    builder = CustomUser.objects.get(email='test_builder_123@mail.com')
    house = House.objects.get(description = "description_test_1")
    house.builder = builder
    house.save()
    needfull_accomodation = Accomodation.objects.get(number=1, house=house)
    url = f'/ads/accomodation/{needfull_accomodation.id}/'
    response = create_builder_user_and_authenticate_fixture.get(url, response='json')
    assert response.status_code == 200


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

    p = Path(__file__).parent
    fileaddress = p.joinpath('test_data', 'test_image_2.jpg')
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


@pytest.mark.django_db
def test_delete_accomodation(generate_multiple_accomodations_fixture,\
                            create_builder_user_and_authenticate_fixture):
    
    builder = CustomUser.objects.get(email='test_builder_123@mail.com')
    house = House.objects.get(description = "description_test_1")
    house.builder = builder
    house.save()
    needfull_accomodation = Accomodation.objects.get(number=1, house=house)
    url = f'/ads/accomodation/{needfull_accomodation.id}/'
    response = create_builder_user_and_authenticate_fixture.delete(url, response='json')
    needfull_accomodation = Accomodation.objects.filter(number=1, house=house)
    assert response.status_code == 204
    assert len(needfull_accomodation) == 0


@pytest.mark.django_db
def test_booking_appartment_by_buider(create_simple_user_and_authenticate_fixture,
                                      generate_multiple_accomodations_fixture,
                                      create_builder_user_and_authenticate_fixture):
    
    builder = CustomUser.objects.get(email='test_builder_123@mail.com')
    house = House.objects.get(description = "description_test_1")
    house.builder = builder
    house.save()
    needfull_accomodation = Accomodation.objects.get(number=1, house=house)
    simple_user = CustomUser.objects.get(email='test123_email@mail.com')
    url = f'/ads/booked_accomodation/{needfull_accomodation.id}'
    payload = {
        "booked_by": simple_user.id
    }
    old_booked_data = needfull_accomodation.booked_by
    response = create_builder_user_and_authenticate_fixture\
                .patch(url, payload, response='json')
    needfull_accomodation.refresh_from_db()
    new_booked_data = needfull_accomodation.booked_by
    assert response.status_code == 200
    assert old_booked_data != new_booked_data


# =============================================================================================
# ===========================ADS==CRUD==ViewSetLogic===========================================
# =============================================================================================


@pytest.mark.django_db
def  test_list_multiple_ads_with_non_moderated_accomodations\
    (generate_multiple_ads_with_non_moderated_accomodations_fixture,\
     create_builder_user_and_authenticate_fixture):
    builder = CustomUser.objects.get(email='test_builder_123@mail.com')
    house = House.objects.get(description = "description_test_1")
    house.builder = builder
    house.save()

    url = f'/ads/ads/'

    response = create_builder_user_and_authenticate_fixture.get(url, response='json')
    assert response.status_code == 200


@pytest.mark.django_db
def  test_create_ads_with_non_moderated_accomodations\
    (generate_multiple_ads_with_non_moderated_accomodations_and_payloads_for_new_objects_fixture,\
     create_builder_user_and_authenticate_fixture):
    builder = CustomUser.objects.get(email='test_builder_123@mail.com')
    house = House.objects.get(description = "description_test_1")
    house.builder = builder
    house.save()

    url = f'/ads/ads/'

    payload = generate_multiple_ads_with_non_moderated_accomodations_and_payloads_for_new_objects_fixture\
                                                                                    .data['new_ads_payload']
    payload = json.dumps(payload, indent=4)
    response = create_builder_user_and_authenticate_fixture.post\
                                            (url, payload, content_type="application/json", response='json')
    assert response.status_code == 201


@pytest.mark.django_db
def  test_retreave_multiple_ads_with_non_moderated_accomodations\
    (generate_multiple_ads_with_non_moderated_accomodations_fixture,\
     create_builder_user_and_authenticate_fixture):
    builder = CustomUser.objects.get(email='test_builder_123@mail.com')
    house = House.objects.get(description = "description_test_1")
    house.builder = builder
    house.save()

    first_ads = Ads.objects.get(accomodation__house=house, accomodation__number=1)
    url = f'/ads/ads/{first_ads.id}/'

    response = create_builder_user_and_authenticate_fixture.get(url, response='json')
    assert response.status_code == 200


@pytest.mark.django_db
def  test_put_ads_with_non_moderated_accomodations\
    (generate_multiple_ads_with_non_moderated_accomodations_fixture,\
    create_builder_user_and_authenticate_fixture):
    builder = CustomUser.objects.get(email='test_builder_123@mail.com')
    house = House.objects.get(description = "description_test_1")
    house.builder = builder
    house.save()

    current_ads = Ads.objects.get(accomodation__house=house, accomodation__number=1)

    old_cost = current_ads.cost
    old_agent_commission = current_ads.agent_commission
    old_cost_per_metter = current_ads.cost_per_metter

    put_payload = {
        'accomodation': current_ads.accomodation.id,
        'cost': 190000,
        'agent_commission': 3,
        'cost_per_metter': 33.1
    }

    put_payload = json.dumps(put_payload, indent=4)
    url = f'/ads/ads/{current_ads.id}/'
    response = create_builder_user_and_authenticate_fixture.put(url, put_payload,\
                                    content_type="application/json", response='json')

    current_ads.refresh_from_db()
    new_cost = current_ads.cost
    new_agent_comission = current_ads.agent_commission
    new_cost_per_metter = current_ads.cost_per_metter

    assert response.status_code == 200
    assert old_cost != new_cost
    assert old_agent_commission != new_agent_comission
    assert old_cost_per_metter != new_cost_per_metter


@pytest.mark.django_db
def  test_patch_ads_with_non_moderated_accomodations\
    (generate_multiple_ads_with_non_moderated_accomodations_fixture,\
    create_builder_user_and_authenticate_fixture):
    builder = CustomUser.objects.get(email='test_builder_123@mail.com')
    house = House.objects.get(description = "description_test_1")
    house.builder = builder
    house.save()

    current_ads = Ads.objects.get(accomodation__house=house, accomodation__number=1)

    old_cost = current_ads.cost

    put_payload = {
        'accomodation': current_ads.accomodation.id,
        'cost': 190000,
    }
    put_payload = json.dumps(put_payload, indent=4)
    url = f'/ads/ads/{current_ads.id}/'
    response = create_builder_user_and_authenticate_fixture.patch(url, put_payload,\
                                    content_type="application/json", response='json')
    current_ads.refresh_from_db()
    new_cost = current_ads.cost

    assert response.status_code == 200
    assert old_cost != new_cost


@pytest.mark.django_db
def  test_delete_ads_with_non_moderated_accomodations\
    (generate_multiple_ads_with_non_moderated_accomodations_fixture,\
     create_builder_user_and_authenticate_fixture):
    builder = CustomUser.objects.get(email='test_builder_123@mail.com')
    house = House.objects.get(description = "description_test_1")
    house.builder = builder
    house.save()

    ads_for_delete = Ads.objects.filter(accomodation__house=house).first()
    old_ads_quantity = Ads.objects.filter(accomodation__house=house).count()
    url = f'/ads/ads/{ads_for_delete.id}/'

    response = create_builder_user_and_authenticate_fixture.delete(url, response='json')
    new_ads_quantity = Ads.objects.filter(accomodation__house=house).count()

    assert response.status_code == 204
    assert old_ads_quantity -1 == new_ads_quantity


# =============================================================================================
# ===========================ADS==FEED=========================================================
# =============================================================================================


@pytest.mark.django_db
def  test_ads_feed_with_moderated_accomodations\
    (generate_multiple_moderated_ads_accomodations_fixture,\
     create_builder_user_and_authenticate_fixture):
    builder = CustomUser.objects.get(email='test_builder_123@mail.com')
    house = House.objects.get(description = "description_test_1")
    house.builder = builder
    house.save()

    url = f'/ads/ads-feed/'
    response = create_builder_user_and_authenticate_fixture.get(url, response='json')
    assert response.status_code == 200


@pytest.mark.django_db
def  test_ads_feed_with_moderated_accomodations_and_multiple_not_pre_created_filters\
    (generate_multiple_moderated_ads_accomodations_fixture,\
     create_builder_user_and_authenticate_fixture):
    builder = CustomUser.objects.get(email='test_builder_123@mail.com')
    house = House.objects.get(description = "description_test_1")
    house.builder = builder
    house.save()

    url = f'/ads/ads-feed/'

    payload = {
        'type_status': 'resale_property',
        'disctrict': 'district_1',
        'microdisctrict': 'mikrodistrict_1',
        'filter_from_cost': 125000,
        'filter_to_cost': 210000,
        'filter_from_area': 50,
        'filter_to_area': 80,
        'filter_house_status': 'appartments',
        'filter_living_condition': 'need_repair',
        'filter_type': 'new_building'
    }

    payload = json.dumps(payload, indent=4)

    response = create_builder_user_and_authenticate_fixture\
                            .post(url, payload, content_type="application/json",\
                                   response='json')

    assert response.status_code == 200



@pytest.mark.django_db
def  test_ads_feed_with_moderated_accomodations_and_single_not_pre_created_filter\
    (generate_multiple_moderated_ads_accomodations_fixture,\
     create_builder_user_and_authenticate_fixture):
    builder = CustomUser.objects.get(email='test_builder_123@mail.com')
    house = House.objects.get(description = "description_test_1")
    house.builder = builder
    house.save()

    url = f'/ads/ads-feed/'

    payload = {
        'type_status': 'resale_property'
    }

    payload = json.dumps(payload, indent=4)

    response = create_builder_user_and_authenticate_fixture\
                            .post(url, payload, content_type="application/json",\
                                   response='json')

    assert response.status_code == 200


@pytest.mark.django_db
def  test_ads_feed_with_moderated_accomodations_and_multiple_not_pre_created_filters_and_filter_save\
    (generate_multiple_moderated_ads_accomodations_fixture,\
     create_builder_user_and_authenticate_fixture):
    builder = CustomUser.objects.get(email='test_builder_123@mail.com')
    house = House.objects.get(description = "description_test_1")
    house.builder = builder
    house.save()

    url = f'/ads/ads-feed/'
    payload = {
        'type_status': 'resale_property',
        'disctrict': 'district_1',
        'microdisctrict': 'mikrodistrict_1',
        'filter_from_cost': 125000,
        'filter_to_cost': 220000,
        'filter_from_area': 50,
        'filter_to_area': 80,
        'filter_house_status': 'appartments',
        'filter_living_condition': 'need_repair',
        'filter_type': 'new_building',
        'save_current_filter': 'true'
    }
    payload = json.dumps(payload, indent=4)

    response = create_builder_user_and_authenticate_fixture\
                            .post(url, payload, content_type="application/json",\
                                   response='json')
    assert response.status_code == 200



@pytest.mark.django_db
def  test_ads_feed_with_moderated_accomodations_and_multiple_not_pre_created_filters_and_filter_save\
    (generate_multiple_moderated_ads_accomodations_fixture,\
    create_builder_user_and_authenticate_fixture,
    create_simple_user_and_authenticate_fixture):
    builder = CustomUser.objects.get(email='test_builder_123@mail.com')
    house = House.objects.get(description = "description_test_1")
    house.builder = builder
    house.save()

    user = CustomUser.objects.get(email='test123_email@mail.com')

    url = f'/ads/ads-feed/'
    filter_data = {
        'filter_type_status': 'resale_property',
        'filter_disctrict': 'district_1',
        'filter_microdisctrict': 'mikrodistrict_1',
        'filter_from_cost': 125000,
        'filter_to_cost': 220000,
        'filter_from_area': 50,
        'filter_to_area': 80,
        'filter_house_status': 'appartments',
        'filter_living_condition': 'need_repair',
        'filter_type': 'new_building',
        'user': user
    }

    filter = Filter(**filter_data)
    filter.save()

    payload = {
        "save_current_filter": filter.id
    }


    payload = json.dumps(payload, indent=4)

    response = create_simple_user_and_authenticate_fixture\
                            .post(url, payload, content_type="application/json",\
                                   response='json')

    assert response.status_code == 200
    assert len(response.data) != 0



# =============================================================================================
# ===========================ADS==LIST====FAVOURITES===========================================
# =============================================================================================

@pytest.mark.django_db
def  test_feed_with_favourite_moderated_ads\
    (generate_multiple_moderated_ads_with_favourites_for_simple_user_fixture):
    url = f'/ads/ads_list_favourites/'
    response = generate_multiple_moderated_ads_with_favourites_for_simple_user_fixture.get(url, response='json')
    assert response.status_code == 200
    assert len(response.data) == 2


@pytest.mark.django_db
def  test_add_ads_to_favourite\
    (generate_multiple_moderated_ads_with_one_favourites_for_simple_user_fixture):
    house = House.objects.get(description="description_test_1")
    ads = Ads.objects.get(accomodation__house=house, favorites_for=None)
    url = f'/ads/ads_retreave_or_add_to_favourite/{ads.id}/'
    payload = {
        'add_to_favourite': True
    }
    response = generate_multiple_moderated_ads_with_one_favourites_for_simple_user_fixture\
        .patch(url, payload, response='json')
    assert response.status_code == 200

@pytest.mark.django_db
def  test_delete_ads_in_favourite\
    (generate_multiple_moderated_ads_with_one_favourites_for_simple_user_fixture):
    house = House.objects.get(description="description_test_1")
    ads = Ads.objects.filter(accomodation__house=house).exclude(favorites_for=None).first()
    url = f'/ads/ads_retreave_or_add_to_favourite/{ads.id}/'
    payload = {
        'add_to_favourite': False
    }
    response = generate_multiple_moderated_ads_with_one_favourites_for_simple_user_fixture\
        .patch(url, payload, response='json')
    assert response.status_code == 200
    assert len(ads.favorites_for.all()) == 0


@pytest.mark.django_db
def test_if_favourite_None_in_serializer_in_favourite\
    (generate_multiple_moderated_ads_with_one_favourites_for_simple_user_fixture):
    house = House.objects.get(description="description_test_1")
    ads = Ads.objects.filter(accomodation__house=house).exclude(favorites_for=None).first()
    url = f'/ads/ads_retreave_or_add_to_favourite/{ads.id}/'
    payload = {}
    response = generate_multiple_moderated_ads_with_one_favourites_for_simple_user_fixture\
        .patch(url, payload, response='json')
    assert response.status_code == 200
    assert len(ads.favorites_for.all()) == 1



# =============================================================================================
# ===========================ADS=====PROMO=====================================================
# =============================================================================================


@pytest.mark.django_db
def test_change_promo_data_for_ads\
            (generate_multiple_moderated_ads_accomodations_fixture,
             create_builder_user_and_authenticate_fixture,
             promotion_create_additional_phrase_fixture
             ):
    builder = CustomUser.objects.get(email='test_builder_123@mail.com')
    house = House.objects.get(description = "description_test_1")
    house.builder = builder
    house.save()

    ads = Ads.objects.filter(accomodation__house=house)[1]
    needfull_promo = PromoAdditionalPhrase.objects.get(text="Super!")
    url = f'/ads/ads_promo_update/{ads.id}'
    payload = {
        "promotion_additional_phrase": needfull_promo.id,
        "is_bigger": True
    }
    response = create_builder_user_and_authenticate_fixture.patch(url, payload, response='json')
    ads.refresh_from_db()
    assert response.status_code == 200
    assert ads.promotion_additional_phrase.text == needfull_promo.text