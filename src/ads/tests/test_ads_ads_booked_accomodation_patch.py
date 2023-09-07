import pytest
from users.models import CustomUser
from houses.models import House
from ads.models import Accomodation
from pathlib import Path
import base64
import json


@pytest.mark.django_db
def test_booking_appartment_by_buider(generate_multiple_accomodations_fixture,
                                      create_builder_user_and_authenticate_fixture,
                                      create_simple_user_and_authenticate_fixture):
    
    builder = CustomUser.objects.get(email='test_builder_123@mail.com')
    house = House.objects.get(description = "description_test_1")
    house.builder = builder
    house.save()
    needfull_accomodation = Accomodation.objects.get(number=1, house=house)
    simple_user = CustomUser.objects.get(email='test123_email@mail.com')
    url = f'/ads/booked_accomodation/{needfull_accomodation.id}'
    payload = {
        "booked_by": simple_user.id
    }
    old_booked_data = needfull_accomodation.booked_by
    response = create_builder_user_and_authenticate_fixture\
                .patch(url, payload, response='json')
    needfull_accomodation.refresh_from_db()
    new_booked_data = needfull_accomodation.booked_by
    assert response.status_code == 200
    assert old_booked_data != new_booked_data
