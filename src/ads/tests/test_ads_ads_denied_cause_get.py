import pytest
from ads.models import DeniedCause

@pytest.mark.django_db
def test_get_of_denied_cause(denied_cause_create_multiple_with_admin_user):
    denied_cause = DeniedCause.objects.get(text="denied_cause_1")
    url = f'/ads/denied_cause/{denied_cause.id}/'
    response = denied_cause_create_multiple_with_admin_user.get(url, response='json')
    assert response.status_code == 200