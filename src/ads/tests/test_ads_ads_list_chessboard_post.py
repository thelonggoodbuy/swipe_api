import pytest
from users.models import CustomUser
from houses.models import House
from ads.models import Ads
import json




@pytest.mark.django_db
def test_filter_cheesboard_for_ads(chesboard_multiple_fixture,
                                   create_builder_user_and_authenticate_fixture):
    builder = CustomUser.objects.get(email='test_builder_123@mail.com')
    house = House.objects.get(description = "description_test_1")
    house.builder = builder
    house.save()

    url = f'/ads/ads_list_chessboard/{house.id}'
    payload = {
        "cost_per_metter_from": 5,
        "cost_per_metter_to": 14,
    }
    response = create_builder_user_and_authenticate_fixture.post(url, payload, response='json')
    assert response.status_code == 200
