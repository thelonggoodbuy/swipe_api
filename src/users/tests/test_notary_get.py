import pytest
from faker import Faker
from users.models import Notary
fake = Faker()


@pytest.mark.django_db
def test_retreave_notary_by_simpe_user(create_user_and_authenticate_fixture):

    payload_notary = {
        'name': fake.name(),
        'surname': fake.name(),
        'phone': fake.phone_number(),
        'email': fake.email(),
    }
    notary = Notary.objects.create(name=fake.name(),
                                    surname=fake.name(),
                                    phone=fake.phone_number(),
                                    email=fake.email())
    url = f'/users/notary/{notary.id}/'
    response = create_user_and_authenticate_fixture.get(url)
    assert response.status_code == 200