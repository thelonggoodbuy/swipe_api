



@pytest.fixture
def create_user_new_fixture(db):
    new_user = CustomUser.objects.create(
        password='test_email@mail.com',
        email='test123_email@mail.com'
        )
    
    client = APIClient()
    refresh = RefreshToken.for_user(new_user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return client



@pytest.mark.django_db
def test_user_detail(create_user_new_fixture):

    user = CustomUser.objects.get(email="test123_email@mail.com")
    url = f'/users/simple_user_update_and_detail/{user.id}/'
    response = create_user_new_fixture.get(url, format='json')
    assert response.status_code == 200