from django.db import models

from houses.models import HouseBuilding, HouseEntrance, Floor, Riser, Document
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
    image_field = models.ManyToManyField('ImageGalery')
    schema = models.ImageField(null=True, blank=True, upload_to="galery/appartment_schemas/")
    booked_by = models.ForeignKey("users.User", on_delete=models.SET_NULL, blank=True, null=True)
    document = models.ManyToManyField(Document)



class ImageGalery(models.Model):
    image = models.ImageField(null=True, blank=True, upload_to="galery/image_galery/")


class Ads(models.Model):
    PROMOTION_COLOR_BOOST_CORT = (
        ("червоний", 'red'),
        ("зелений", 'green'),
        ("немає", 'None'),
    )
    CHOICES_CORT = (
        ("не модеровано", 'non_moderated'),
        ("прийнято", 'approved'),
        ("відхилено", 'denied'),
    )
    VERSION_OF_CALCULATION_CORT = (
        ("кредит", 'credit'),
        ("тільки готівка", 'only_cash'),
        ("іпотека", 'mortgage'),
    )
    accomodation = models.OneToOneField(Accomodation, on_delete=models.SET_NULL, null=True, blank=True)
    agent_commission = models.DecimalField(max_digits=10, decimal_places=2)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    cost_per_metter = models.DecimalField(max_digits=10, decimal_places=2)
    promotion_additional_phrase = models.ForeignKey('PromoAdditionalPhrase', on_delete=models.SET_NULL, null=True, blank=True)
    promotion_color_boost = models.CharField(max_length=200, choices=PROMOTION_COLOR_BOOST_CORT, default=PROMOTION_COLOR_BOOST_CORT[2][1])
    ads_status = models.CharField(max_length=200, choices=CHOICES_CORT, default=CHOICES_CORT[0][1])
    denied_cause = models.ForeignKey('DeniedCause', on_delete=models.SET_NULL, null=True, blank=True)
    version_of_calculation = models.CharField(max_length=200, choices=VERSION_OF_CALCULATION_CORT,)


class DeniedCause(models.Model):
    text = models.CharField(max_length=400)


class PromoAdditionalPhrase(models.Model):
    text = models.CharField(max_length=400)