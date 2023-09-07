import pytest
from users.models import CustomUser
from houses.models import House
from ads.models import Ads, Filter
import json





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