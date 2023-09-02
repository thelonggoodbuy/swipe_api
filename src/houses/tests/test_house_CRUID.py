# ---------------------FIXTURES----------------------------------
import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import CustomUser
from django.conf import settings
import environ
import os

from pathlib import Path
from faker import Faker

env = environ.Env()
environ.Env.read_env(env_file=os.path.join(settings.BASE_DIR, ".env.dev"))

fake = Faker()


@pytest.fixture(scope='function')
def django_db_setup():
    settings.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env("POSTGRES_TEST_DB"),
        'USER': env("POSTGRES_TEST_USER"),
        'PASSWORD': env("POSTGRES_TEST_PASSWORD"),
        "HOST": env("POSTGRES_HOST"),
        "PORT": env("POSTGRES_PORT"),
    }


@pytest.fixture
def api_client_fixture():
    client = APIClient()
    return client


@pytest.fixture
def create_builder_user_and_authenticate_fixture(db):
    payload = {
        "email": "test_builder_123@mail.com",
        "is_builder": True,
        "is_activated": True,
    }
    test_user = CustomUser(**payload)
    test_user.set_password("test_password")
    test_user.save()
    client = APIClient()
    refresh = RefreshToken.for_user(test_user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return client



@pytest.fixture
def generate_data_for_creating_house_fixture(db):

    payload = {
        "description": "description_test_1",
        "address": "address_test_1",
        "disctrict": "district_1",
        "microdisctrict": "mikrodistrict_1",
        "house_status": "appartments",
        "house_type": "flats",
        "house_class": "mainstreem",
        "building_technology": "monoblock",
        "square_type": "closed_with_guard",
        "distance_to_sea": 215,
        "services_payment": "payments",
        "ceiling_height": 3,
        "household_gas": "yes",
        "heating": "central",
        "sewage": "central",
        "plumbing": "central",
        "sales_department_name": fake.name(),
        "sales_department_surname": fake.name(),
        "sales_department_phone": "+380611111234",
        "sales_department_email": fake.email(),
        "registration": "international",
        "type_of_account": "credit",
        "purpose": "dwelling",
        "summ_of_threaty": "not_a_complete",
        "image_field": []
    }
    p = Path(__file__).parent
    fileaddress = p.joinpath('test_data', 'image.jpg')
    image_file = open(fileaddress, 'rb')
    payload['main_image'] = image_file

    client = APIClient()
    payload_user = {
        "email": "test_builder_123@mail.com",
        "is_builder": True,
        "is_activated": True,
    }
    test_user = CustomUser(**payload_user)
    test_user.set_password("test_password")
    test_user.save()
    client = APIClient()
    refresh = RefreshToken.for_user(test_user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    client.data = {"house_payload": payload}
    return client

    # return client

from houses.models import House

@pytest.fixture
def generate_house_fixture(db):

    payload = {
        "description": "description_test_1",
        "address": "address_test_1",
        "disctrict": "district_1",
        "microdisctrict": "mikrodistrict_1",
        "house_status": "appartments",
        "house_type": "flats",
        "house_class": "mainstreem",
        "building_technology": "monoblock",
        "square_type": "closed_with_guard",
        "distance_to_sea": 215,
        "services_payment": "payments",
        "ceiling_height": 3,
        "household_gas": "yes",
        "heating": "central",
        "sewage": "central",
        "plumbing": "central",
        "sales_department_name": fake.name(),
        "sales_department_surname": fake.name(),
        "sales_department_phone": "+380611111234",
        "sales_department_email": fake.email(),
        "registration": "international",
        "type_of_account": "credit",
        "purpose": "dwelling",
        "summ_of_threaty": "not_a_complete",
    }

    house = House(**payload)
    house.save()
    client = APIClient()    
    return client


@pytest.fixture
def generate_multiple_house_fixture(db):

    payload = {
        "description": "description_test_1",
        "address": "address_test_1",
        "disctrict": "district_1",
        "microdisctrict": "mikrodistrict_1",
        "house_status": "appartments",
        "house_type": "flats",
        "house_class": "mainstreem",
        "building_technology": "monoblock",
        "square_type": "closed_with_guard",
        "distance_to_sea": 215,
        "services_payment": "payments",
        "ceiling_height": 3,
        "household_gas": "yes",
        "heating": "central",
        "sewage": "central",
        "plumbing": "central",
        "sales_department_name": fake.name(),
        "sales_department_surname": fake.name(),
        "sales_department_phone": "+380611111234",
        "sales_department_email": fake.email(),
        "registration": "international",
        "type_of_account": "credit",
        "purpose": "dwelling",
        "summ_of_threaty": "not_a_complete",
    }

    house = House(**payload)
    house.save()
    house = House(**payload)
    house.save()

    client = APIClient()    
    return client


# --------------------------------------------------------------


import pytest
from users.models import CustomUser
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from users.tokens import user_activation_token




@pytest.mark.django_db
def test_simple_user_activation_registration(api_client_fixture):
    # Testing email confirmation with creation simple user.
    url = '/users/auth/register_simple_user/'
    payload = {
        "email": "test_user@gmail.com",
        "password": "test_password_123!@",
        "is_simple_user": True,
    }
    response = api_client_fixture.post(url, payload, response='json')
    user = CustomUser.objects.get(email='test_user@gmail.com')
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = user_activation_token.make_token(user)
    activation_url = f'/users/auth/activate_simple_user/{uid}/{token}/'
    response_for_activation = api_client_fixture.get(activation_url)
    user.refresh_from_db()
    assert user.is_activated == True
    assert response_for_activation.status_code == 200



@pytest.mark.django_db
def test_create_house(generate_data_for_creating_house_fixture):
    url = f'/houses/houses/'
    payload = generate_data_for_creating_house_fixture.data['house_payload']
    response = generate_data_for_creating_house_fixture.post(url, payload, response='json')
    assert response.status_code == 201



@pytest.mark.django_db
def test_update_house(create_builder_user_and_authenticate_fixture,\
                      generate_house_fixture):
    house = House.objects.get(description = "description_test_1")
    builder = CustomUser.objects.get(email='test_builder_123@mail.com')
    house.builder = builder
    house.save()
    url = f'/houses/houses/{house.id}/'
    payload = {"address": "address_test_2"}
    response = create_builder_user_and_authenticate_fixture.patch(url, payload, response='json')
    assert response.status_code == 200
    payload = {"address": "address_test_3"}
    response = create_builder_user_and_authenticate_fixture.put(url, payload, response='json')
    assert response.status_code == 200


@pytest.mark.django_db
def test_retreave_house(create_builder_user_and_authenticate_fixture,\
                      generate_house_fixture):
    house = House.objects.get(description = "description_test_1")
    builder = CustomUser.objects.get(email='test_builder_123@mail.com')
    house.builder = builder
    house.save()
    url = f'/houses/houses/{house.id}/'
    response = create_builder_user_and_authenticate_fixture.get(url, response='json')
    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_house(create_builder_user_and_authenticate_fixture,\
                      generate_house_fixture):
    house = House.objects.get(description = "description_test_1")
    builder = CustomUser.objects.get(email='test_builder_123@mail.com')
    house.builder = builder
    house.save()
    url = f'/houses/houses/{house.id}/'
    response = create_builder_user_and_authenticate_fixture.delete(url)
    assert response.status_code == 204


@pytest.mark.django_db
def test_list_house(generate_multiple_house_fixture,\
                    create_builder_user_and_authenticate_fixture):
    
    builder = CustomUser.objects.get(email='test_builder_123@mail.com')
    for house in House.objects.filter(description='description_test_1'):
        house.builder = builder
        house.save()
    houses_list = House.objects.filter(builder=builder)
    assert houses_list.count() == 2



