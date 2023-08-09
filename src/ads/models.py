from django.db import models

from houses.models import HouseBuilding, HouseEntrance, Floor, Riser, Document, House
# from users.models import User


# Create your models here.
class Accomodation(models.Model):
    TYPE_CORT = (
        ("новобудова", "new_building"),
        ("вторинне житло", "resale_property"),
        ("коттедж", "cottage"),
    )
    PLANNING_CORT = (
        ("студія з санвузлом", "studio_appartment_with_barhroom"),
        ("студія з санвузлом і однією спальнею", "studio_appartment_with_barhroom_and_one bedroom"),
        ("двокімнатна", "two_bedroom"),
        ("двокімнатна зі своєю кришею", "two_bedroom_and_roof"),
        ("трьокімнатна", "three_vedroom"),
        ("трьокімнатна зі своєю кришею", "three_vedroom_and_roof"),
    )
    LIVING_CONDITION_CORT = (
        ('вимагає ремонту', 'need_repair'),
        ('готова для заселення', 'reary_for_settlement'),
    )
    HEAT_TYPE_CORT = (
        ('газове', 'gas'),
        ('електричний', 'electric'),
        ("дров'яне опалення", 'wood_heating'),
    )
    type_status = models.CharField(max_length=200, choices=TYPE_CORT)
    number = models.PositiveSmallIntegerField()
    house = models.ForeignKey(House, on_delete=models.CASCADE, related_name='accomodation')
    house_building = models.ForeignKey(HouseBuilding, on_delete=models.SET_NULL, blank=True, null=True)
    house_entrance = models.ForeignKey(HouseEntrance, on_delete=models.SET_NULL, blank=True, null=True)
    floor = models.ForeignKey(Floor, on_delete=models.SET_NULL, blank=True, null=True)
    riser = models.ForeignKey(Riser, on_delete=models.SET_NULL, blank=True, null=True)
    area = models.DecimalField(max_digits=6, decimal_places=2)
    planing = models.CharField(max_length=200, choices=PLANNING_CORT)
    living_condition = models.CharField(max_length=200, choices=LIVING_CONDITION_CORT)
    area_kitchen = models.DecimalField(max_digits=6, decimal_places=2)
    have_balcony = models.BooleanField()
    heat_type = models.CharField(max_length=200, choices=HEAT_TYPE_CORT)
    image_field = models.ManyToManyField('ImageGalery', related_name='accomodation')
    schema = models.ImageField(null=True, blank=True, upload_to="galery/appartment_schemas/")
    booked_by = models.ForeignKey("users.CustomUser", on_delete=models.SET_NULL, blank=True, null=True)
    document = models.ManyToManyField(Document)
    date_added = models.DateField(auto_now_add=True)



class ImageGalery(models.Model):
    image = models.ImageField(null=True, blank=True, upload_to="galery/image_galery/")


class Ads(models.Model):
    PROMOTION_COLOR_BOOST_CORT = (
        ('red', "червоний"),
        ('green', "зелений"),
        ('None', "немає"),
    )
    CHOICES_CORT = (
        ('non_moderated', "не модеровано"),
        ('approved', "прийнято"),
        ('denied', "відхилено"),
    )
    VERSION_OF_CALCULATION_CORT = (
        ('credit', "кредит"),
        ('only_cash', "тільки готівка"),
        ('mortgage', "іпотека"),
    )
    accomodation = models.OneToOneField(Accomodation, on_delete=models.SET_NULL, null=True, blank=True)
    agent_commission = models.DecimalField(max_digits=10, decimal_places=2)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    cost_per_metter = models.DecimalField(max_digits=10, decimal_places=2)
    promotion_additional_phrase = models.ForeignKey('PromoAdditionalPhrase', on_delete=models.SET_NULL, null=True, blank=True)
    promotion_color_boost = models.CharField(max_length=200, choices=PROMOTION_COLOR_BOOST_CORT, default=PROMOTION_COLOR_BOOST_CORT[2][0], null=True, blank=True)
    ads_status = models.CharField(max_length=200, choices=CHOICES_CORT, default=CHOICES_CORT[0][0])
    denied_cause = models.ForeignKey('DeniedCause', on_delete=models.SET_NULL, null=True, blank=True)
    version_of_calculation = models.CharField(max_length=200, choices=VERSION_OF_CALCULATION_CORT, default=VERSION_OF_CALCULATION_CORT[2][0])
    date_added = models.DateTimeField(auto_now_add=True)


class DeniedCause(models.Model):
    text = models.CharField(max_length=400)


class PromoAdditionalPhrase(models.Model):
    text = models.CharField(max_length=400)