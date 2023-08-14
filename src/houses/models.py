from django.db import models

# from ads.models import ImageGalery

# from users.models import User
# Create your models here.




class House(models.Model):
    HOUSE_STATUS_CORT = (
        ("appartments", "квартири"),
        ("appartments_with_terrace", "квартири з терассами"),
        ("penthouse", "пентхауз"),
        ("individual_house", "індивідуальний будинок"),
    )
    HOUSE_TYPE_CORT = (
        ("flats", "багатоквартирним"),
        ("townhouse", "таунхауз"),
        ("cottage", "коттедж"),
    )
    HOUSE_CLASS_CORT = (
        ("elite", "елітний"),
        ("mainstreem", "мейнстрім"),
        ("econom+", "економ+"),
    )
    BUILDING_TECHNOLOGY_CORT = (
        ("monoblock", "моноблок"),
        ("brick_and_slab", "цегла та плити"),
        ("brick_and_wood", "цегла та деревина"),
    )
    SQUARE_TYPE_CORT = (
        ("closed_with_guard", "закрита з охороною"),
        ("closed_with_watchman", "закрита з вахтером"),
        ("open_with_watchman", "відкрита з вахтером"),
    )
    SERVICES_PAYMENT_CORT = (
        ("payments", "Платежи"),
        ("management_company", "керуюча компанія"),
    )
    HOUSEHOLD_GAS_CORT = (
        ("yes", "є"),
        ("no", "ні"),
        ("only_heating", "тільки опалення"),
    )
    HEATING_CORT = (
        ("central", "центральне"),
        ("individual", "індивідуальне"),
    )
    SEWAGE_CORT = (
        ("central", "центральне"),
        ("individual", "індивідуальна", ),
    )
    PLUMBING_CORT = (
        ("central", "центральне"),
        ("individual", "індивідуальна"),
    )
    REGISTRARION_CORT = (
        ("judiciary", "юстиція"),
        ("international", "міжнарода"),
    )
    ACCOUNT_CORT = (
        ("mortrage", "іпотека"),
        ("credit", "кредит"),
        ("full_account", "полная"),
        ("prepfyment_with_discount", "предоплата со скидкой"),
    )
    PURPOSE_CORT = (
        ("dwelling", "житлова"),
        ("commercial", "торгівельна"),
    )
    SUMM_OF_THREADY_CORT = (
        ("not_a_complete", "не повна"),
        ("full", "повна"),
    )
    description = models.TextField()
    address = models.CharField(max_length=200)
    disctrict = models.CharField(max_length=200, null=True, blank=True)
    microdisctrict = models.CharField(max_length=200, null=True, blank=True)
    house_status = models.CharField(max_length=200, choices=HOUSE_STATUS_CORT, blank=True, null=True)
    house_type = models.CharField(max_length=200, choices=HOUSE_TYPE_CORT)
    house_class = models.CharField(max_length=200, choices=HOUSE_CLASS_CORT)
    building_technology = models.CharField(max_length=200, choices=BUILDING_TECHNOLOGY_CORT)
    square_type = models.CharField(max_length=200, choices=SQUARE_TYPE_CORT)
    distance_to_sea = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    services_payment = models.CharField(max_length=200, choices=SERVICES_PAYMENT_CORT)
    ceiling_height = models.DecimalField(max_digits=10, decimal_places=2)
    household_gas = models.CharField(max_length=200, choices=HOUSEHOLD_GAS_CORT)
    heating = models.CharField(max_length=200, choices=HEATING_CORT)
    sewage = models.CharField(max_length=200, choices=SEWAGE_CORT)
    plumbing = models.CharField(max_length=200, choices=PLUMBING_CORT)
    # sales_department = models.ForeignKey("users.CustomUser", on_delete=models.SET_NULL, blank=True, null=True)
    sales_department_name = models.CharField(max_length=200, blank=True, null=True)
    sales_department_surname = models.CharField(max_length=200, blank=True, null=True)
    sales_department_phone = models.CharField(max_length=200, blank=True, null=True)
    sales_department_email = models.EmailField(max_length=200, blank=True, null=True)
    registration = models.CharField(max_length=200, choices=REGISTRARION_CORT)
    type_of_account = models.CharField(max_length=200, choices=ACCOUNT_CORT)
    purpose = models.CharField(max_length=200, choices=PURPOSE_CORT)
    summ_of_threaty = models.CharField(max_length=200, choices=SUMM_OF_THREADY_CORT)
    main_image = models.ImageField(null=True, blank=True, upload_to="galery/houses_main_images/")
    image_field = models.ManyToManyField('ads.ImageGalery', related_name='house')
    location = models.CharField(max_length=2500, null=True, blank=True)
    builder = models.ForeignKey("users.CustomUser", on_delete=models.SET_NULL, blank=True, null=True, related_name='house')
    # date_added = models.DateField(auto_now_add=True)
    
    
class AdvantagePerHouse(models.Model):
    house = models.ManyToManyField(House)
    title = models.CharField(max_length=200)
    
    
class HouseBuilding(models.Model):
    house = models.ForeignKey(House, on_delete=models.SET_NULL, blank=True, null=True, related_name='house_building')
    title = models.CharField(max_length=200)

    
class HouseEntrance(models.Model):
    house = models.ForeignKey(House, on_delete=models.SET_NULL, blank=True, null=True, related_name='house_entrance')
    title = models.CharField(max_length=200)

    
class Floor(models.Model):
    house = models.ForeignKey(House, on_delete=models.SET_NULL, blank=True, null=True, related_name='floor')
    title = models.CharField(max_length=200)
    floor_schema = models.ImageField(null=True, blank=True, upload_to="galery/floor_schemas/")


class Riser(models.Model):
    house = models.ForeignKey(House, on_delete=models.SET_NULL, blank=True, null=True, related_name='riser')
    title = models.CharField(max_length=200)
    

class Document(models.Model):
    title = models.CharField(max_length=200)
    floor_schema = models.ImageField(null=True, blank=True, upload_to="documents/")
    
    
class NewsPerHouse(models.Model):
    house = models.ForeignKey(House, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=200)