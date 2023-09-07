import pytest
from users.models import CustomUser
from houses.models import House
import json
from ads.models import Ads


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
