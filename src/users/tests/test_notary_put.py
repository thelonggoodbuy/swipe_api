import pytest

from faker import Faker
from users.models import Notary

fake = Faker()


@pytest.mark.django_db
def test_update_notary_by_admin(create_admin_user_and_authenticate_fixture):
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
    response = create_admin_user_and_authenticate_fixture.post(url, payload_notary, response='json')
    payload_put_notary = {
        'name': 'test_notary_2',
        'surname': fake.name(),
        'phone': fake.phone_number(),
        'email': fake.email(),
    }
    response_put_update = create_admin_user_and_authenticate_fixture.put(url, payload_put_notary, response='json')
    assert response_put_update.status_code == 200

    payload_patch_notary = {
        'name': 'test_notary_3',
        'surname': fake.name(),
        'phone': fake.phone_number(),
        'email': fake.email(),
    }
    response_patch_update = create_admin_user_and_authenticate_fixture.patch(url, payload_patch_notary, response='json')
    assert response_patch_update.status_code == 200