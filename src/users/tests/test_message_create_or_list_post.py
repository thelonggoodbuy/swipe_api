import pytest
from faker import Faker
fake = Faker()

@pytest.mark.django_db
def test_create_message(create_user_and_authenticate_fixture):
    # Test POST request to send message to tehnical
    # support.
    url = f'/users/message_create_or_list/'
    payload = {
        'message_text': fake.text(),
    }
    response = create_user_and_authenticate_fixture.post(url, payload, response='json')
    assert response.status_code == 201