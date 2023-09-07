import pytest

@pytest.mark.django_db
def test_create_house(generate_data_for_creating_house_fixture):
    url = f'/houses/houses/'
    payload = generate_data_for_creating_house_fixture.data['house_payload']
    response = generate_data_for_creating_house_fixture.post(url, payload, response='json')
    assert response.status_code == 201