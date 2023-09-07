import pytest

@pytest.mark.django_db
def test_list_of_denied_cause(denied_cause_create_multiple_with_admin_user):
    url = f'/ads/denied_cause/'
    response = denied_cause_create_multiple_with_admin_user.get(url, response='json')
    assert response.status_code == 200