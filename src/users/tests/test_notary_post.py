import pytest

from faker import Faker

fake = Faker()




@pytest.mark.django_db
def test_create_notary_by_admin(create_admin_user_and_authenticate_fixture):
    url = f'/users/notary/'
    payload_notary = {
        'name': fake.name(),
        'surname': fake.name(),
        'phone': fake.phone_number(),
        'email': fake.email(),
    }
    response = create_admin_user_and_authenticate_fixture.post(url, payload_notary, response='json')
    assert response.status_code == 201
