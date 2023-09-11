from faker import Faker
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
import random

from houses.models import House, AdvantagePerHouse, HouseBuilding,\
                            HouseEntrance, Floor, Riser

from users.models import CustomUser
from ads.models import Accomodation, Ads, ImageGalery, DeniedCause, PromoAdditionalPhrase
from pathlib import Path
from django.core.files.uploadedfile import SimpleUploadedFile

fake = Faker('uk_UA')

class Command(BaseCommand):
    help = 'Ads and accomodation objects initialization'
    def handle(self, *args, **kwargs):
        initial_builder = CustomUser.objects.get(email="initial_builder@gmail.com")

        try:
            initial_builder = CustomUser.objects.get(email="initial_builder@gmail.com")
            if Accomodation.objects.filter(house__builder=initial_builder).count() == 0:

                initial_house = House.objects.get(builder=initial_builder)
                area_values = [39, 46.5, 51.4, 59.3, 75]
                area_kitchen_values = [10, 12, 14, 20]
                file_title_list = ['initial_image_1.jpg', 'initial_image_2.jpg',
                                'initial_image_3.jpg', 'initial_image_4.jpg',
                                'initial_image_5.jpg', 'initial_image_6.jpg',
                                'initial_image_7.jpg']
                house_building_list = list(initial_house.house_building.all())
                house_entrance_list = list(initial_house.house_entrance.all())
                floor_list = list(initial_house.floor.all())
                riser_list = list(initial_house.riser.all())

                agent_comission_list = [0.09, 0.1, 0.15, 0.25]
                cost_list = [450000, 500000, 550000, 600000, 650000]

                for index in range(1, 13):
                    accomodation = Accomodation(
                        type_status="new_building",
                        number=index,
                        house=initial_house,
                        house_building=random.choice(house_building_list),
                        house_entrance=random.choice(house_entrance_list),
                        floor=random.choice(floor_list),
                        riser=random.choice(riser_list),
                        area=random.choice(area_values),
                        planing="two_bedroom",
                        living_condition="reary_for_settlement",
                        area_kitchen=random.choice(area_kitchen_values),
                        have_balcony=True,
                        heat_type='gas',
                        is_shown_in_chesboard=True
                    )
                    accomodation.save()

                    p = Path(__file__).parents[4]
                    filetitle = random.choice(file_title_list)
                    fileaddress = p.joinpath('seed/initial_data/images', filetitle)
                    with open(fileaddress, 'rb') as infile:
                        _file = SimpleUploadedFile(filetitle, infile.read())
                        accomodation.schema = _file
                        accomodation.save()

                    filetitle = random.choice(file_title_list)
                    fileaddress = p.joinpath('seed/initial_data/images', filetitle)
                    with open(fileaddress, 'rb') as infile:
                        _file = SimpleUploadedFile(filetitle, infile.read())
                        image = ImageGalery.objects.create(image=_file, obj_order=1)
                        accomodation.image_field.add(image)
                        accomodation.save()

                    filetitle = random.choice(file_title_list)
                    fileaddress = p.joinpath('seed/initial_data/images', filetitle)
                    with open(fileaddress, 'rb') as infile:
                        _file = SimpleUploadedFile(filetitle, infile.read())
                        image = ImageGalery.objects.create(image=_file, obj_order=2)
                        accomodation.image_field.add(image)
                        accomodation.save()

                    ads = Ads(
                        agent_commission=0.1,
                        cost=random.choice(agent_comission_list),
                        cost_per_metter=random.choice(cost_list),
                        version_of_calculation='credit'
                    )
                    ads.save()
                    ads.accomodation = accomodation
                    ads.save()

                    if DeniedCause.objects.all().count() == 0:
                        denied_list = ["Некорректна ціна", "Некоректне фото",
                                       "Некорректний опис", "Iнше"]
                        for cause_text in denied_list: DeniedCause.objects.create(text=cause_text)

                    if PromoAdditionalPhrase.objects.all().count() == 0:
                        promo_phrases = ["Подарунок при покупці", "Торг є можливим",
                                         "Квартира біля моря", "В спальному районі",
                                         "Вам повезло з ціною!", "Для великої родини",
                                         "Родинне гніздо", "Окрема парковка"]
                        for promo_phrase in promo_phrases: PromoAdditionalPhrase.objects.create(text=promo_phrase)

                print('================================================')
                print('----You--have--created--initial-accomodation----')
                print('--and-ads and-others--subbordinate--objects-----')
                print('================================================')


        except ObjectDoesNotExist:
            print('================================================')
            print('-----------initial--ADS--script-----------------')
            print('--WASNT--TRIGGERED-by-initial_builder@gmail.com-')
            print('--------------It--DOESN`T--EXIST----------------')
            print('================================================')
            pass