import pytest
from users.models import CustomUser
from houses.models import House
from ads.models import DeniedCause

from pathlib import Path
import base64

@pytest.mark.django_db
def test_delete_of_denied_cause(denied_cause_create_multiple_with_admin_user):
    denied_cause = DeniedCause.objects.get(text="denied_cause_1")
    url = f'/ads/denied_cause/{denied_cause.id}/'
    response = denied_cause_create_multiple_with_admin_user.delete(url, response='json')
    assert response.status_code == 204