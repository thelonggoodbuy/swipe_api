import pytest
from users.models import CustomUser
from houses.models import House
from ads.models import Ads
import json



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
