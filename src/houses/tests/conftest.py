import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import CustomUser
from django.conf import settings
import environ
import os
env = environ.Env()
environ.Env.read_env(env_file=os.path.join(settings.BASE_DIR, ".env.dev"))




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


import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import CustomUser
from django.conf import settings
import environ
import os

from houses.models import HouseEntrance, Floor, HouseBuilding, Riser

from houses.models import House

from pathlib import Path
from faker import Faker

env = environ.Env()
environ.Env.read_env(env_file=os.path.join(settings.BASE_DIR, ".env.dev"))

fake = Faker()

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
def generate_house_fixture_with_subordinate_objects_fixture(db):

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

    first_entrance = HouseEntrance.objects.create(house=house, title='first_entrance')
    first_entrance.save()

    second_entrance = HouseEntrance.objects.create(house=house, title='second_entrance')
    second_entrance.save()

    first_floor = Floor.objects.create(house=house, title='first_floor')
    first_floor.save()

    second_floor = Floor.objects.create(house=house, title='second_floor')
    second_floor.save()

    first_house_building = HouseBuilding.objects.create(house=house, title='first_house_building')
    first_house_building.save()

    second_house_building = HouseBuilding.objects.create(house=house, title='second_house_building')
    second_house_building.save()

    first_house_riser = Riser.objects.create(house=house, title='first_house_riser')
    first_house_riser.save()

    second_house_riser = Riser.objects.create(house=house, title='second_house_riser')
    second_house_riser.save()

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

