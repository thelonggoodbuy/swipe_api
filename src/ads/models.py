from django.db import models

from houses.models import HouseBuilding, HouseEntrance, Floor, Riser, Document, House
# from users.models import User


# Create your models here.
class Accomodation(models.Model):
    TYPE_CORT = (
        ("new_building", "новобудова"),
        ("resale_property", "вторинне житло"),
        ("cottage", "коттедж"),
    )
    PLANNING_CORT = (
        ("studio_appartment_with_barhroom", "студія з санвузлом"),
        ("studio_appartment_with_barhroom_and_one bedroom", "студія з санвузлом і однією спальнею"),
        ("two_bedroom", "двокімнатна"),
        ("two_bedroom_and_roof", "двокімнатна зі своєю кришею"),
        ("three_vedroom", "трьокімнатна"),
        ("three_vedroom_and_roof", "трьокімнатна зі своєю кришею"),
    )
    LIVING_CONDITION_CORT = (
        ('need_repair', 'вимагає ремонту'),
        ('reary_for_settlement', 'готова для заселення'),
    )
    HEAT_TYPE_CORT = (
        ('gas', 'газове'),
        ('electric', 'електричний'),
        ('wood_heating', "дров'яне опалення"),
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
    is_shown_in_chesboard = models.BooleanField()



class ImageGalery(models.Model):
    image = models.ImageField(null=True, blank=True, upload_to="galery/image_galery/")
    obj_order = models.SmallIntegerField(blank=True, null=True)

    # def __str__(self):
    #     return self.image.url


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
    accomodation = models.OneToOneField(Accomodation, on_delete=models.SET_NULL, null=True, blank=True, related_name='ads')
    agent_commission = models.DecimalField(max_digits=10, decimal_places=2)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    cost_per_metter = models.DecimalField(max_digits=10, decimal_places=2)
    ads_status = models.CharField(max_length=200, choices=CHOICES_CORT, default=CHOICES_CORT[0][0])
    denied_cause = models.ForeignKey('DeniedCause', on_delete=models.SET_NULL, null=True, blank=True)
    version_of_calculation = models.CharField(max_length=200, choices=VERSION_OF_CALCULATION_CORT, default=VERSION_OF_CALCULATION_CORT[2][0])
    date_added = models.DateTimeField(auto_now_add=True)
    is_bigger = models.BooleanField(null=True, blank=True)
    is_lifted_in_feed = models.BooleanField(null=True, blank=True)
    is_turbo = models.BooleanField(null=True, blank=True)
    promotion_additional_phrase = models.ForeignKey('PromoAdditionalPhrase', on_delete=models.SET_NULL, null=True, blank=True)
    promotion_color_boost = models.CharField(max_length=200, choices=PROMOTION_COLOR_BOOST_CORT, default=PROMOTION_COLOR_BOOST_CORT[2][0], null=True, blank=True)
    favorites_for = models.ManyToManyField('users.CustomUser', related_name='favourites_adds')


class DeniedCause(models.Model):
    text = models.CharField(max_length=400)


class PromoAdditionalPhrase(models.Model):
    text = models.CharField(max_length=400)


class Filter(models.Model):
    TYPE_CORT = (
        ("new_building", "новобудова"),
        ("resale_property", "вторинне житло"),
        ("cottage", "коттедж"),
    )
    HOUSE_STATUS_CORT = (
        ("appartments", "квартири"),
        ("appartments_with_terrace", "квартири з терассами"),
        ("penthouse", "пентхауз"),
        ("individual_house", "індивідуальний будинок"),
    )
    LIVING_CONDITION_CORT = (
        ('need_repair', 'вимагає ремонту'),
        ('reary_for_settlement', 'готова для заселення'),
    )
    FILTER_TYPE_CORT = (
        ('all', 'всі'),
        ('resale_property', 'вторинне житло'),
        ('new_buiding', 'новобудова'),
        ('cottage', 'коттедж')
    )
    user = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE)
    filter_type_status = models.CharField(max_length=200, choices=TYPE_CORT, blank=True, null=True)
    filter_disctrict = models.CharField(max_length=200, blank=True, null=True)
    filter_microdisctrict = models.CharField(max_length=200, blank=True, null=True)
    filter_from_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    filter_to_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    filter_from_area = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    filter_to_area = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    filter_house_status = models.CharField(max_length=200, choices=HOUSE_STATUS_CORT, blank=True, null=True)
    filter_living_condition = models.CharField(max_length=200, choices=LIVING_CONDITION_CORT, blank=True, null=True)
    filter_type = models.CharField(max_length=200, choices=FILTER_TYPE_CORT)

    def return_filter_dict(self):
        fields = Filter._meta.get_fields()
        print('====FILEDS====')
        # print(fields)
        # print(self.__dict__.values('filter_type_status'))
        print('==============')
        # dictionary = {}
        # return print