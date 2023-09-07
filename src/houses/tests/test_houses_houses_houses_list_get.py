import pytest
from users.models import CustomUser
from houses.models import House


@pytest.mark.django_db
def test_list_house(generate_multiple_house_fixture,\
                    create_builder_user_and_authenticate_fixture):
    
    builder = CustomUser.objects.get(email='test_builder_123@mail.com')
    for house in House.objects.filter(description='description_test_1'):
        house.builder = builder
        house.save()
    houses_list = House.objects.filter(builder=builder)
    assert houses_list.count() == 2
    url = f'/houses/houses/'
    response = create_builder_user_and_authenticate_fixture.get(url, response='json')
    assert response.status_code == 200