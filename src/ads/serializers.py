from rest_framework import serializers


from .models import Accomodation, ImageGalery, Ads, DeniedCause


from houses.models import House, HouseBuilding, HouseEntrance,\
                    Floor, Riser
from users.models import CustomUser

from drf_extra_fields.fields import Base64ImageField



class PhotoToAccomodationSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=False)

    class Meta:
        model = ImageGalery
        fields = ['id', 'image']


class AccomodationSerializer(serializers.ModelSerializer):
    house = serializers.PrimaryKeyRelatedField(required=True, queryset = House.objects.all())
    house_building = serializers.PrimaryKeyRelatedField(required=False, queryset = HouseBuilding.objects.all())
    house_entrance = serializers.PrimaryKeyRelatedField(required=False, queryset = HouseEntrance.objects.all())
    floor = serializers.PrimaryKeyRelatedField(required=False, queryset = Floor.objects.all())
    riser = serializers.PrimaryKeyRelatedField(required=False, queryset = Riser.objects.all())
    image_field = PhotoToAccomodationSerializer(many=True, required=False)
    booked_by = serializers.PrimaryKeyRelatedField(required=False, queryset = CustomUser.objects.all())

    class Meta:
        model = Accomodation
        fields = ['id', 'type_status', 'number',\
                'house', 'house_building', 'house_entrance',\
                'floor', 'riser', 'area', 'planing',\
                'living_condition', 'area_kitchen', 'have_balcony',\
                'heat_type', 'image_field', 'booked_by']
        
    def create(self, validated_data):
        if 'image_field' in validated_data:
            photo_data = validated_data.pop('image_field')
        accomodation_obj = Accomodation.objects.create(**validated_data)
        try:
            for photo_obj in photo_data:
                photo_fields = dict(photo_obj)
                image = ImageGalery.objects.create(**photo_fields)
                image.save()
                accomodation_obj.image_field.add(image)
        except NameError:
            pass
        
        accomodation_obj.save()
        return accomodation_obj
    
    def update(self, instance, validated_data):
        if 'image_field' in validated_data:
            photo_data = validated_data.pop('image_field')
            ImageGalery.objects.filter(accomodation=instance).delete()

        for item in validated_data:
            if Accomodation._meta.get_field(item):
                setattr(instance, item, validated_data[item])

        try:
            photo_data
        except NameError:
            return instance
        else:
            for photo_obj in photo_data:
                photo_fields = dict(photo_obj)
                image = ImageGalery.objects.create(**photo_fields)
                image.save()
                instance.image_field.add(image)
        instance.save()
        return instance
    

    def validate(self, data):
        current_house = data['house']
        if current_house.accomodation.filter(number=data['number']).exists():
            raise serializers.ValidationError("Номер квартири має бути унікальним для цього будинку. Квартира з таким номером вже зареєстрована")
        if data['house_building'] not in current_house.house_building.all():
            raise serializers.ValidationError("Ви повинні обрати корпус, який знаходиться в цьому будинку.")
        if data['house_entrance'] not in current_house.house_entrance.all():
            raise serializers.ValidationError("Ви повинні обрати підїзд, який знаходиться в цьому будинку.")
        if data['floor'] not in current_house.floor.all():
            raise serializers.ValidationError("Ви повинні обрати поверх, який знаходиться в цьому будинку.")
        if data['riser'] not in current_house.riser.all():
            raise serializers.ValidationError("Ви повинні обрати стояк, який знаходиться в цьому будинку.")

        return data
    


class AdsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ads
        fields = ['accomodation', 'agent_commission', 'cost',
                  'cost_per_metter', 'version_of_calculation']
        
    def validate(self, data):
        request = self.context.get("request")
        if (data['accomodation'] not in Accomodation.objects.filter(house__builder=request.user))\
            and request.user.is_superuser == False:
            raise serializers.ValidationError("Змінювати такий тип данних може тільки забудовник, або адмін.")

        return data
    


class AdsAccomodationDataSerializer(serializers.ModelSerializer):
    floor_quantity = serializers.SerializerMethodField()
    floor_title = serializers.SerializerMethodField()
    house_address = serializers.SerializerMethodField()
    house_disctrict = serializers.SerializerMethodField()

    class Meta:
        model = Accomodation
        fields = ['planing', 'area', 'floor_title', 'floor_quantity', 'house_address', 'house_disctrict']

    def get_floor_quantity(self, obj):
        floor_quantity = obj.house.floor.all().count()
        return floor_quantity
    
    def get_floor_title(self, obj):
        floor_title = obj.floor.title
        return floor_title
    
    def get_house_address(self, obj):
        house_address=obj.house.address
        return house_address
    
    def get_house_disctrict(self, obj):
        house_district=obj.house.disctrict
        return house_district


class AdsListModerationSerializer(serializers.ModelSerializer):
    accomodation = AdsAccomodationDataSerializer(many=False, required=False)

    class Meta:
        model = Ads
        fields = ['cost', 'accomodation', 'version_of_calculation', 'date_added']
        # depth = 1






class DeniedCauseSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeniedCause
        fields = ['text',]