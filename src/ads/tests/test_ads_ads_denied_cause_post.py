import pytest



@pytest.mark.django_db
def test_create_of_denied_cause(denied_cause_create_multiple_with_admin_user):
    url = f'/ads/denied_cause/'
    payload = {'text': 'New_cause_text'}
    response = denied_cause_create_multiple_with_admin_user.post(url, payload, response='json')
    assert response.status_code == 201
