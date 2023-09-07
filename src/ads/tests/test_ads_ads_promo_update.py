import pytest
from users.models import CustomUser
from houses.models import House
from ads.models import Ads, PromoAdditionalPhrase
import json





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
