import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import CustomUser, Subscription
from django.conf import settings
from django.utils import timezone
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


# --------------------SIMPLE--USER-REGISTRATION-AND-AUTHENTICATION-FIXTURES------------------
@pytest.fixture
def create_user_and_authenticate_fixture(db):
    payload = {
        "email": "test123_email@mail.com",
        "is_simple_user": True,
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
def api_client_fixture():
    client = APIClient()
    return client



@pytest.fixture
def create_user_without_authentication_fixture(db):
    new_user = CustomUser.objects.create(
        email='test123_email@mail.com',
        is_simple_user = True,
        is_activated = True,
        )
    new_user.set_password("test_password")
    client = APIClient()
    return client

# --------------------ADMIN--USER-REGISTRATION-AND-AUTHENTICATION-FIXTURES------------------
@pytest.fixture
def create_admin_user_and_authenticate_fixture(db):
    payload = {
        "email": "test123_email@mail.com",
        "is_superuser": True,
        "is_staff": True,
        "is_activated": True,
    }
    test_user = CustomUser(**payload)
    test_user.set_password("test_password")
    test_user.save()
    client = APIClient()
    refresh = RefreshToken.for_user(test_user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return client

# ---------------------------USER-SUBSCRIPTION-FIXTURES----------------------------------





@pytest.fixture
def create_user_with_subscription_fixture(db):
    payload = {
        "email": "test123_email@mail.com",
        "is_simple_user": True,
        "is_activated": True,
    }
    test_user = CustomUser(**payload)
    test_user.set_password("test_password")
    

    new_subscription = Subscription()
    new_subscription.is_auto_renewal = False

    new_subscription.subscription_last_date = timezone.now()
    new_subscription.is_active = True
    new_subscription.save()
    test_user.subscription = new_subscription
    test_user.save()

    client = APIClient()
    refresh = RefreshToken.for_user(test_user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return client



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
    fileaddress = p.joinpath('seed/test_data/images', 'test_image_7.jpg')
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



import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import CustomUser
from django.conf import settings
import environ
import os
import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import CustomUser
from django.conf import settings
import environ
import os
from houses.models import HouseEntrance, Floor, HouseBuilding, Riser, House
from pathlib import Path
from faker import Faker

from ads.models import PromoAdditionalPhrase, DeniedCause

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
def create_builder_user_and_authenticate_fixture(db: None):
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
def create_simple_user_and_authenticate_fixture(db: None):
    payload = {
        "email": "test123_email@mail.com",
        "is_simple_user": True,
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
def create_admin_user_and_authenticate_fixture(db: None):
    payload = {
        "email": "test_admin_123@mail.com",
        "is_superuser": True,
        "is_activated": True,
        "is_staff": True
    }
    test_user = CustomUser(**payload)
    test_user.set_password("test_password")
    test_user.save()
    client = APIClient()
    refresh = RefreshToken.for_user(test_user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return client


@pytest.fixture
def generate_data_for_creating_house_fixture(db: None):

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
    fileaddress = p.joinpath('seed/test_data/images', 'test_image_7.jpg')
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
def generate_house_fixture(db: None):

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
def generate_house_fixture_with_subordinate_objects_fixture(db: None):

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
def generate_multiple_house_fixture(db: None):

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



# ================================================================
# ======================ACCOMODATION==============================
# ================================================================
from ads.models import Accomodation, Ads
import base64
from django.core.files.uploadedfile import SimpleUploadedFile
from ads.models import ImageGalery

@pytest.fixture
def generate_multiple_accomodations_fixture(db: None):
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

    first_payload = {
        'type_status': 'new_building',
        'number': 1,
        'house': house,
        'house_building': first_house_building,
        'house_entrance': second_entrance,
        'floor': first_floor,
        'riser': first_house_riser,
        'area': 65,
        'planing': 'two_bedroom',
        'living_condition': 'need_repair',
        'area_kitchen': 18,
        'have_balcony': True,
        'heat_type': 'electric',
        'is_shown_in_chesboard': False
    }
    first_acomodation = Accomodation(**first_payload)

    p = Path(__file__).parent
  
    fileaddress = p.joinpath('seed/test_data/images', 'test_image_1.jpg')
    with open(fileaddress, 'rb') as infile:
        _file = SimpleUploadedFile('test_image_1.jpg', infile.read())
        first_acomodation.schema = _file
        first_acomodation.save()

    fileaddress = p.joinpath('seed/test_data/images', 'test_image_2.jpg')
    with open(fileaddress, 'rb') as infile:
        _file = SimpleUploadedFile('test_image_2.jpg', infile.read())
        first_image = ImageGalery.objects.create(image=_file, obj_order=0)
        first_image.save()
        first_acomodation.image_field.add(first_image)

    fileaddress = p.joinpath('seed/test_data/images', 'test_image_3.jpg')
    with open(fileaddress, 'rb') as infile:
        _file = SimpleUploadedFile('test_image_3.jpg', infile.read())
        second_image = ImageGalery.objects.create(image=_file, obj_order=1)
        second_image.save()
        first_acomodation.image_field.add(second_image)

    first_acomodation.save()

    second_payload = {
        'type_status': 'resale_property',
        'number': 2,
        'house': house,
        'house_building': first_house_building,
        'house_entrance': second_entrance,
        'floor': first_floor,
        'riser': first_house_riser,
        'area': 78,
        'planing': 'two_bedroom',
        'living_condition': 'need_repair',
        'area_kitchen': 12,
        'have_balcony': True,
        'heat_type': 'electric',
        # image_field: add Base64 string,
        # schema: add Base64 string,
        'is_shown_in_chesboard': False
    }
    second_acomodation = Accomodation(**second_payload)

    fileaddress = p.joinpath('seed/test_data/images', 'test_image_3.jpg')
    with open(fileaddress, 'rb') as infile:
        _file = SimpleUploadedFile('test_image_3.jpg', infile.read())
        second_acomodation.schema = _file
        second_acomodation.save()

    fileaddress = p.joinpath('seed/test_data/images', 'test_image_2.jpg')
    with open(fileaddress, 'rb') as infile:
        _file = SimpleUploadedFile('test_image_2.jpg', infile.read())
        first_image = ImageGalery.objects.create(image=_file, obj_order=0)
        first_image.save()
        second_acomodation.image_field.add(first_image)

    fileaddress = p.joinpath('seed/test_data/images', 'test_image_1.jpg')
    with open(fileaddress, 'rb') as infile:
        _file = SimpleUploadedFile('test_image_1.jpg', infile.read())
        second_image = ImageGalery.objects.create(image=_file, obj_order=1)
        second_image.save()
        second_acomodation.image_field.add(second_image)
    
    second_acomodation.save()

    client = APIClient()    
    return client



# -------------------------------------------------------------------------
# -----------------------ADS----TESTS--------------------------------------
# -------------------------------------------------------------------------


@pytest.fixture
def generate_multiple_ads_with_non_moderated_accomodations_fixture(generate_multiple_accomodations_fixture):

    house = House.objects.get(description="description_test_1")

    accomodations = house.accomodation.all()
    first_accomodation = accomodations[0]
    second_accomodation = accomodations[1]

    first_ads_payload = {
        'accomodation': first_accomodation,
        'agent_commission': 1,
        'cost': 200000,
        'cost_per_metter': 15.6,
        'ads_status': 'non_moderated',
        'version_of_calculation': 'credit'
    }
    first_ads = Ads(**first_ads_payload)
    first_ads.save()

    second_ads_payload = {
        'accomodation': second_accomodation,
        'agent_commission': 0.5,
        'cost': 150000,
        'cost_per_metter': 11.2,
        'ads_status': 'non_moderated',
        'version_of_calculation': 'credit'
    }
    second_ads = Ads(**second_ads_payload)
    second_ads.save()

    client = APIClient()

    client.data = {}
    client.data['new_objects_id'] = [first_ads, second_ads]

        
    return client



@pytest.fixture
def generate_multiple_ads_with_non_moderated_accomodations_and_payloads_for_new_objects_fixture\
    (generate_multiple_ads_with_non_moderated_accomodations_fixture):

    house = House.objects.get(description="description_test_1")

    new_appartment_payload = {
        'type_status': 'new_building',
        'number': 3,
        'house': house,
        'house_building': house.house_building.all().first(),
        'house_entrance': house.house_entrance.all().first(),
        'floor': house.floor.all().first(),
        'riser': house.riser.all().first(),
        'area': 81,
        'planing': 'two_bedroom',
        'living_condition': 'need_repair',
        'area_kitchen': 12,
        'have_balcony': True,
        'heat_type': 'electric',
        # image_field: add Base64 string,
        # schema: add Base64 string,
        'is_shown_in_chesboard': False
    }

    new_appartment = Accomodation(**new_appartment_payload)
    new_appartment.save()

    new_ads_payload = {
        'accomodation': new_appartment.id,
        'agent_commission': 0.5,
        'cost': 150000,
        'cost_per_metter': 11.2,
        'ads_status': 'non_moderated',
        'version_of_calculation': 'credit'
    }

    client = APIClient()
    client.data = {}
    client.data['new_ads_payload'] = new_ads_payload
    return client



@pytest.fixture
def generate_multiple_moderated_ads_accomodations_fixture\
    (generate_multiple_ads_with_non_moderated_accomodations_fixture):

    house = House.objects.get(description="description_test_1")

    ads_list = Ads.objects.filter(accomodation__house=house)

    first_ads = ads_list[0]
    first_ads.ads_status = 'approved'
    first_ads.save()

    second_ads = ads_list[1]
    second_ads.ads_status = 'approved'
    second_ads.save()

    client = APIClient()
    client.data = {}
    client.data['ads_quantity'] = ads_list.count()
    return client


@pytest.fixture
def generate_multiple_moderated_ads_with_favourites_for_simple_user_fixture\
    (generate_multiple_ads_with_non_moderated_accomodations_fixture,
     create_simple_user_and_authenticate_fixture):

    house = House.objects.get(description="description_test_1")
    ads_list = Ads.objects.filter(accomodation__house=house)

    simple_user = CustomUser.objects.get(email="test123_email@mail.com")

    first_ads = ads_list[0]
    first_ads.ads_status = 'approved'
    first_ads.favorites_for.add(simple_user)
    first_ads.save()

    second_ads = ads_list[1]
    second_ads.ads_status = 'approved'
    second_ads.favorites_for.add(simple_user)
    second_ads.save()

    client = APIClient()
    client.data = {}
    client.data['simple_user_id'] = simple_user.id

    refresh = RefreshToken.for_user(simple_user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    return client


@pytest.fixture
def generate_multiple_moderated_ads_with_one_favourites_for_simple_user_fixture\
    (generate_multiple_ads_with_non_moderated_accomodations_fixture,
     create_simple_user_and_authenticate_fixture):

    house = House.objects.get(description="description_test_1")
    ads_list = Ads.objects.filter(accomodation__house=house)

    simple_user = CustomUser.objects.get(email="test123_email@mail.com")

    first_ads = ads_list[0]
    first_ads.ads_status = 'approved'
    first_ads.favorites_for.add(simple_user)
    first_ads.save()

    second_ads = ads_list[1]
    second_ads.ads_status = 'approved'
    # second_ads.favorites_for.add(simple_user)
    second_ads.save()

    client = APIClient()
    client.data = {}
    client.data['simple_user_id'] = simple_user.id

    refresh = RefreshToken.for_user(simple_user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    return client


# --------------------------------------------------------------------------
# ---------------------------promo---additional-----phrases-----------------
# --------------------------------------------------------------------------

@pytest.fixture
def promotion_create_additional_phrase_fixture():

    PromoAdditionalPhrase.objects.create(text="Super!")
    PromoAdditionalPhrase.objects.create(text="Nice!")
    PromoAdditionalPhrase.objects.create(text="Go Go Go!")

    client = APIClient()
    return client


# ---------------------------------------------------------------------------
# -------------------------chesboard-----------------------------------------
# ---------------------------------------------------------------------------

@pytest.fixture()
def chesboard_multiple_fixture(generate_multiple_moderated_ads_accomodations_fixture):
    house = House.objects.get(description="description_test_1")
    ads_list = Ads.objects.filter(accomodation__house=house)

    first_ads = ads_list[0]
    first_ads.ads_status = 'approved'
    first_ads.accomodation.is_shown_in_chesboard = True
    first_ads.accomodation.save()
    first_ads.save()

    second_ads = ads_list[1]
    second_ads.ads_status = 'approved'
    first_ads.accomodation.is_shown_in_chesboard = True
    first_ads.accomodation.save()
    second_ads.save()

    client = APIClient()
    client.data = {}
    client.data['ads_quantity'] = ads_list.count()
    return client


# ---------------------------------------------------------------------------
# -------------------------denied---causes-----------------------------------
# ---------------------------------------------------------------------------


@pytest.fixture
def denied_cause_create_multiple_with_admin_user(create_admin_user_and_authenticate_fixture):

    denied_cause_1 = DeniedCause.objects.create(text="denied_cause_1")
    denied_cause_2 = DeniedCause.objects.create(text="denied_cause_2")

    admin = CustomUser.objects.get(email="test_admin_123@mail.com")
    refresh = RefreshToken.for_user(admin)
    client = APIClient()

    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    
    return client