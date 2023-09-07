import pytest

@pytest.mark.django_db
def test_get_all_ads_for_moderation(create_admin_user_and_authenticate_fixture,
                                    generate_multiple_ads_with_non_moderated_accomodations_and_payloads_for_new_objects_fixture):
    url = f'/ads/moderation_ads/'
    response = create_admin_user_and_authenticate_fixture.get(url, response='json')
    assert response.status_code == 200