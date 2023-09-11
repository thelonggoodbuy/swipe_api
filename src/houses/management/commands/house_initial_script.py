from faker import Faker
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand

from houses.models import House, AdvantagePerHouse, HouseBuilding,\
                            HouseEntrance, Floor, Riser

from users.models import CustomUser

fake = Faker('uk_UA')


class Command(BaseCommand):
    help = 'House and subbordinate objects initialization'
    def handle(self, *args, **kwargs):

        try:
            initial_builder = CustomUser.objects.get(email="initial_builder@gmail.com")
            print('================================================')
            print('------You--run--INITIAL--BUILDER----script------')


            house = House(
                description='initial_house',
                address='initial_house_address',
                district='initial_house_district',
                microdisctrict='initial_house_microdisctrict',
                house_status='appartments',
                house_type="flats",
                house_class="mainstreem",
                building_technology="brick_and_slab",
                square_type="open_with_watchman",
                distance_to_sea=150.3,
                services_payment="payments",
                ceiling_height=2.7,
                household_gas="yes",
                heating="individual",
                sewage="individual",
                plumbing="central",
                sales_department_name=fake.name(),
                sales_department_surname=fake.name(),
                sales_department_phone=fake.phone_number(),
                sales_department_email=fake.email(),
                registration="judiciary",
                type_of_account="credit",
                purpose="dwelling",
                summ_of_threaty="full",
                builder=initial_builder
            )
            house.save()
            print('=================================================')
            print('--------INITIAL--HOUSE---CREATED-----------------')
            print(f'-------------------id={house.id}----------------')
            print(f'---------description={house.description}--------')

            for index in range(1,4):
                advantage = AdvantagePerHouse.objects.create(
                    # house=house,
                    title=f"initial_advantage_data_{index}"
                )
                advantage.house.add(house)
                advantage.save()
                print(f'Advantage "{advantage.title}" created')
                print('***')

                house_building = HouseBuilding.objects.create(
                    house=house,
                    title=f"initial_house_building_{index}"
                )
                print(f'House building "{house_building.title}" created')
                print('***')
                
                house_entrance = HouseEntrance.objects.create(
                    house=house,
                    title=f"initial_house_entrance_{index}"
                )
                print(f'House entrance "{house_entrance.title}" created')
                print('***')
                
                floor = Floor.objects.create(
                    house=house,
                    title=f"initial_floor_{index}"
                )
                print(f'House floor "{floor.title}" created')
                print('***')

                riser = Riser.objects.create(
                    house=house,
                    title=f"initial_riser_{index}"
                )
                print(f'Riser "{riser.title}" created')
                print('***')


            print('-------You--have--created--one--house--and------')
            print('----------others--subbordinate--objects---------')
            print('================================================')

        except ObjectDoesNotExist:
            print('================================================')
            print('-----------initial--BUILDER--script-------------')
            print('--WASNT--TRIGGERED-by-initial_builder@gmail.com-')
            print('--------------It--DOESN`T--EXIST----------------')
            print('================================================')
            pass