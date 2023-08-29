import pytest

from faker import Faker
from users.models import Notary

fake = Faker()


@pytest.mark.django_db
def test_delete_notary_by_admin(create_admin_user_and_authenticate_fixture):
    url = f'/users/notary/'
    payload_notary = {
        'name': 'test_notary_1',
        'surname': fake.name(),
        'phone': fake.phone_number(),
        'email': fake.email(),
    }
    create_admin_user_and_authenticate_fixture.post(url, payload_notary, response='json')
    notary = Notary.objects.get(name='test_notary_1')
    url = f'/users/notary/{notary.id}/'
    response_delete = create_admin_user_and_authenticate_fixture.delete(url)
    assert response_delete.status_code == 204