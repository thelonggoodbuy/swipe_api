import pytest
from users.models import CustomUser
from houses.models import House
from ads.models import Ads
import json





@pytest.mark.django_db
def test_chessboard_data_for_ads(chesboard_multiple_fixture,
                                   create_builder_user_and_authenticate_fixture):
    builder = CustomUser.objects.get(email='test_builder_123@mail.com')
    house = House.objects.get(description = "description_test_1")
    house.builder = builder
    house.save()

    url = f'/ads/ads_list_chessboard/{house.id}'
    response = create_builder_user_and_authenticate_fixture.get(url, response='json')

    assert response.status_code == 200
    assert len(response.data) == chesboard_multiple_fixture.data['ads_quantity']

