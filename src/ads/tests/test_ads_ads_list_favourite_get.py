import pytest


@pytest.mark.django_db
def  test_feed_with_favourite_moderated_ads\
    (generate_multiple_moderated_ads_with_favourites_for_simple_user_fixture):
    url = f'/ads/ads_list_favourites/'
    response = generate_multiple_moderated_ads_with_favourites_for_simple_user_fixture.get(url, response='json')
    assert response.status_code == 200
    assert len(response.data) == 2