from faker import Faker
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand

from users.models import CustomUser, Notary

fake = Faker('uk_UA')


class Command(BaseCommand):
    help = 'Users builder and admin initialization'
    def handle(self, *args, **kwargs):

        try:
            CustomUser.objects.get(is_superuser=True, is_activated=True)
        except ObjectDoesNotExist:
            print('================================================')
            print('------You--run--INITIAL--SUPERUSER--script------')
            print('================================================')
            admin_user = CustomUser(
                email="initial_admin@gmail.com",
                is_superuser=True,
                is_staff=True,
                is_activated=True,
                first_name=fake.name(),
                second_name=fake.name(),
            )
            admin_user.set_password('initial_password')
            admin_user.save()
            print('==============================================')
            print('------initial-admin-was-been-created----------')
            print(f'Email is {admin_user.email}.')
            print(f"Password is 'initial_password'")
            print('==============================================')
        

        try:
            CustomUser.objects.get(is_builder=True, is_activated=True)
        except ObjectDoesNotExist:
            print('================================================')
            print('-You--run--INITIAL--BUILDER--AND--SIMPLE-USER-script-')
            print('================================================')
            builder_user = CustomUser(
                email="initial_builder@gmail.com",
                is_builder=True,
                is_activated=True,
                first_name=fake.name(),
                second_name=fake.name(),
            )
            builder_user.set_password('initial_password')
            builder_user.save()
            print('==============================================')
            print('----initial--builder--was--been--created------')
            print(f'Email is {builder_user.email}.')
            print(f"Password is 'initial_password'")
            print('==============================================')

            print('==============================================')
            print('----------SIMPLE--USER--INITIALISATION--------')
            for index in range(1, 4):
                simple_user = CustomUser(
                    email=f"simple_builder_{index}@gmail.com",
                    is_simple_user=True,
                    is_activated=True,
                    first_name=fake.name(),
                    second_name=fake.name(),
                )
                simple_user.set_password('initial_password')
                simple_user.save()
                print(f'Email is {simple_user.email}.')
                print(f"Password is 'initial_password'")
            print('==============================================')


        if Notary.objects.all().count() == 0:
            print('================================================')
            print('------You--run--INITIAL--NOTARY--script------')
            print('================================================')
            notary = Notary(
                name=fake.name(),
                surname='initial_notary',
                phone=fake.phone_number(),
                email=fake.email()
            )
            notary.save()
            print('==============================================')
            print('------initial-notary-was-been-created----------')
            print(f'Name is {notary.name}.')
            print(f'Surname is {notary.surname}.')
            print('==============================================')