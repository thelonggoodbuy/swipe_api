import pytest
from users.models import CustomUser
from houses.models import House
from ads.models import Ads
import json






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

