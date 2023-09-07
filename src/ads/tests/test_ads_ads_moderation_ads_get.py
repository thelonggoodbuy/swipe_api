import pytest
from users.models import CustomUser
from houses.models import House
from ads.models import DeniedCause, Ads

from pathlib import Path
import base64



@pytest.mark.django_db
def test_retreave_ads_for_moderation(create_admin_user_and_authenticate_fixture,
                                    generate_multiple_ads_with_non_moderated_accomodations_fixture,
                                    create_builder_user_and_authenticate_fixture):
    
    builder = CustomUser.objects.get(email='test_builder_123@mail.com')
    house = House.objects.get(description = "description_test_1")
    house.builder = builder
    house.save()

    obj_id = generate_multiple_ads_with_non_moderated_accomodations_fixture.data['new_objects_id'][0].id
    created_ads = Ads.objects.get(id=obj_id)
    url = f'/ads/moderation_ads/{created_ads.id}/'

    response = create_admin_user_and_authenticate_fixture.get(url, response='json')

    assert response.status_code == 200
