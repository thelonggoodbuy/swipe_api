import pytest
from users.models import CustomUser
from houses.models import House
import json

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