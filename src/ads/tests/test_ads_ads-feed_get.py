import pytest
from users.models import CustomUser
from houses.models import House



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