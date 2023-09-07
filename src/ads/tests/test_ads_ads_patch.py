import pytest
from users.models import CustomUser
from houses.models import House
from ads.models import Ads
import json



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
