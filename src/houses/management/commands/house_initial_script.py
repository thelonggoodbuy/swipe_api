# from faker import Faker
# from django.core.exceptions import ObjectDoesNotExist
# from django.core.management.base import BaseCommand

# from houses.models import House

# from users.models import CustomUser

# fake = Faker('uk_UA')


# class Command(BaseCommand):
#     help = 'House and subbordinate objects initialization'
#     def handle(self, *args, **kwargs):

#         try:
#             CustomUser.objects.get(is_superuser=True, is_activated=True)
#         except ObjectDoesNotExist:
#             print('================================================')
#             print('------You--run--INITIAL--SUPERUSER--script------')
#             print('================================================'