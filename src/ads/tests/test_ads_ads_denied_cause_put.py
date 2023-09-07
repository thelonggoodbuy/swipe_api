import pytest
from users.models import CustomUser
from houses.models import House
from ads.models import DeniedCause

from pathlib import Path
import base64


@pytest.mark.django_db
def test_update_of_denied_cause(denied_cause_create_multiple_with_admin_user):
    denied_cause = DeniedCause.objects.get(text="denied_cause_1")
    denied_cause_text = denied_cause.text
    url = f'/ads/denied_cause/{denied_cause.id}/'
    payload = {
        "text": "changed_text_1"
    }
    response = denied_cause_create_multiple_with_admin_user.put(url, payload, response='json')
    denied_cause.refresh_from_db()
    assert response.status_code == 200
    assert denied_cause_text != denied_cause.text