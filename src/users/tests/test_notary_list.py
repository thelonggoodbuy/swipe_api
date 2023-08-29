import pytest
from faker import Faker
from users.models import Notary
fake = Faker()


@pytest.mark.django_db
def test_retreave_list_notary_by_simple_user(create_user_and_authenticate_fixture):

    for i in range (1, 3):
        notary = Notary.objects.create(name='test_notary',
                                        surname=fake.name(),
                                        phone=fake.phone_number(),
                                        email=fake.email())
    url = f'/users/notary/'
    response = create_user_and_authenticate_fixture.get(url)
    assert response.status_code == 200
    assert Notary.objects.filter(name='test_notary').count() == 2