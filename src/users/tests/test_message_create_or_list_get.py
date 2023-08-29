import pytest
from faker import Faker
fake = Faker()

from users.models import Message, CustomUser
from django.db.models import Q


@pytest.mark.django_db
def test_list_of_messages(create_user_and_authenticate_fixture):
    # Test GET request for receiving all messages
    # which have been sent by and to user.
    url = f'/users/message_create_or_list/'
    payload_first_message = {
        'message_text': fake.text(),
    }
    response = create_user_and_authenticate_fixture.post(url, payload_first_message, response='json')
    payload_senond_message = {
        'message_text': fake.text(),
    }
    response = create_user_and_authenticate_fixture.post(url, payload_senond_message, response='json')
    response = create_user_and_authenticate_fixture.get(url)
    user = CustomUser.objects.get(email='test123_email@mail.com')
    assert Message.objects.filter(Q(from_user=user) | Q(to_user=user)).count() == 4
    assert response.status_code == 200