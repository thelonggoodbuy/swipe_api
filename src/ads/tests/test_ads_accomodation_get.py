import pytest
from users.models import CustomUser
from houses.models import House
from ads.models import Accomodation


@pytest.mark.django_db
def test_retreave_accomodation(generate_multiple_accomodations_fixture,\
                            create_builder_user_and_authenticate_fixture):
    
    builder = CustomUser.objects.get(email='test_builder_123@mail.com')
    house = House.objects.get(description = "description_test_1")
    house.builder = builder
    house.save()
    needfull_accomodation = Accomodation.objects.get(number=1, house=house)
    url = f'/ads/accomodation/{needfull_accomodation.id}/'
    response = create_builder_user_and_authenticate_fixture.get(url, response='json')
    assert response.status_code == 200