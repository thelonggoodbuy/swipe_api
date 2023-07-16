from django.db import models


# from users.models import User
# Create your models here.




class House(models.Model):
    HOUSE_STATUS_CORT = (
        ("квартири", "appartments"),
        ("квартири з терассами", "appartments_with_terrace"),
        ("пентхауз", "penthouse"),
    )
    HOUSE_TYPE_CORT = (
        ("багатоквартирним", "flats"),
        ("таунхауз", "townhouse"),
        ("коттедж", "cottage"),
    )
    HOUSE_CLASS_CORT = (
        ("елітний", "elite"),
        ("мейнстрім", "mainstreem"),
        ("економ+", "econom+"),
    )
    BUILDING_TECHNOLOGY_CORT = (
        ("моноблок", "monoblock"),
        ("цегла та плити", "brick_and_slab"),
        ("цегла та деревина", "brick_and_wood"),
    )
    SQUARE_TYPE_CORT = (
        ("закрита з охороною", "closed_with_guard"),
        ("закрита з вахтером", "closed_with_watchman"),
        ("відкрита з вахтером", "open_with_watchman"),
    )
    SERVICES_PAYMENT_CORT = (
        ("Платежи", "payments"),
        ("керуюча компанія", "management_company"),
    )
    HOUSEHOLD_GAS_CORT = (
        ("є", "yes"),
        ("ні", "no"),
        ("тільки опалення", "only_heating"),
    )
    HEATING_CORT = (
        ("центральне", "central"),
        ("індивідуальне", "individual"),
    )
    SEWAGE_CORT = (
        ("центральне", "central"),
        ("індивідуальна", "individual"),
    )
    PLUMBING_CORT = (
        ("центральне", "central"),
        ("індивідуальна", "individual"),
    )
    REGISTRARION_CORT = (
        ("юстиція", "judiciary"),
        ("міжнарода", "international"),
    )
    ACCOUNT_CORT = (
        ("іпотека", "mortrage"),
        ("credit", "кредит"),
        ("full_account", "полная"),
        ("prepfyment_with_discount", "предоплата со скидкой"),
    )
    PURPOSE_CORT = (
        ("житлова", "dwelling"),
        ("торгівельна", "commercial"),
    )
    SUMM_OF_THREADY_CORT = (
        ("не повна", "not_a_complete"),
        ("повна", "full"),
    )
    description = models.TextField()
    address = models.CharField(max_length=200)
    disctrict = models.CharField(max_length=200, null=True, blank=True)
    microdisctrict = models.CharField(max_length=200, null=True, blank=True)
    house_status = models.CharField(max_length=200, choices=HOUSE_STATUS_CORT)
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
    sales_department = models.ForeignKey("users.User", on_delete=models.SET_NULL, blank=True, null=True)
    registration = models.CharField(max_length=200, choices=REGISTRARION_CORT)
    type_of_account = models.CharField(max_length=200, choices=ACCOUNT_CORT)
    purpose = models.CharField(max_length=200, choices=PURPOSE_CORT)
    summ_of_threaty = models.CharField(max_length=200, choices=SUMM_OF_THREADY_CORT)
    main_image = models.ImageField(null=True, blank=True, upload_to="galery/houses_main_images/")
    location = models.CharField(max_length=2500, null=True, blank=True)
    
    
class AdvantagePerHouse(models.Model):
    house = models.ManyToManyField(House)
    title = models.CharField(max_length=200)
    
    
class HouseBuilding(models.Model):
    house = models.ForeignKey(House, on_delete=models.SET_NULL, blank=True, null=True)
    title = models.CharField(max_length=200)

    
class HouseEntrance(models.Model):
    house = models.ForeignKey(House, on_delete=models.SET_NULL, blank=True, null=True)
    title = models.CharField(max_length=200)

    
class Floor(models.Model):
    house = models.ForeignKey(House, on_delete=models.SET_NULL, blank=True, null=True)
    title = models.CharField(max_length=200)
    floor_schema = models.ImageField(null=True, blank=True, upload_to="galery/floor_schemas/")


class Riser(models.Model):
    house = models.ForeignKey(House, on_delete=models.SET_NULL, blank=True, null=True)
    title = models.CharField(max_length=200)
    

class Document(models.Model):
    title = models.CharField(max_length=200)
    floor_schema = models.ImageField(null=True, blank=True, upload_to="documents/")
    
    
class NewsPerHouse(models.Model):
    house = models.ForeignKey(House, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=200)