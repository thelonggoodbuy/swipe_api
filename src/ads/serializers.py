from rest_framework import serializers


from .models import Accomodation, ImageGalery, Ads, DeniedCause


from houses.models import House, HouseBuilding, HouseEntrance,\
                    Floor, Riser
from users.models import CustomUser

from drf_extra_fields.fields import Base64ImageField



class PhotoToAccomodationSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    image = Base64ImageField(required=False)
    obj_order = serializers.IntegerField(required=False)


    class Meta:
        model = ImageGalery
        fields = ['id', 'image', 'obj_order']

    # def to_representation(self, data):

    #     representation = super().to_representation(data)
    #     representation['addition_id'] = data.id

    #     return representation
    

    # def to_internal_value(self, data):
    #     print('======internal=value===')
        
    #     data['addition_id'] = data['id']
    #     print(data)
    #     print('=======================')
    #     # resource_data = data['resource']

    #     return super().to_internal_value(data)


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
            deleted_list = []
            updated_list = []
            list_of_images_id = []

            list_of_dict_images_id = instance.image_field.all().values('id')
            # print('============================')
            # print(list_of_images_id.values())
            for dict_of_image_id in list_of_dict_images_id: list_of_images_id.append(dict_of_image_id['id'])

            # print(validated_data['image_field'])
            # print('===================================')

            
            for image_obj in validated_data['image_field']:
                # print(image_obj)
                
                if 'obj_order' not in image_obj:
                    # print(f'Delete:{image_obj}')
                    delete_obj = image_obj['id']
                    # deleted_list.append(delete_obj)
                    image_obj = ImageGalery.objects.get(id=image_obj['id'])
                    instance.image_field.remove(image_obj)
                    del image_obj

                elif 'id' in image_obj and image_obj['id'] in list_of_images_id:
                    ImageGalery.objects.filter(id=image_obj['id']).update(**image_obj)

                else:

                    new_image = ImageGalery.objects.create(**image_obj)
                    instance.image_field.add(new_image)




                # ==========================================================================================


                # else:
                #     pass
                    # print(image_obj['id'])
                    # updated_obj = image_obj['id']
                    # updated_list.
                #     for photo_obj in photo_data:
                #         photo_fields = dict(photo_obj)
                #         image = ImageGalery.objects.create(**photo_fields)
                #         image.save()
                #         instance.image_field.add(image)
                    # MyModel.objects.filter(pk=some_value).update(field1='some value')
            # print('===========================')
            # print(deleted_list)
            # print(updated_list)
            # print('===========================')


        # if 'image_field' in validated_data:
        #     photo_data = validated_data.pop('image_field')
        #     ImageGalery.objects.filter(accomodation=instance).delete()

        # for item in validated_data:
        #     if Accomodation._meta.get_field(item):
        #         setattr(instance, item, validated_data[item])

        # try:
        #     photo_data
        # except NameError:
        #     return instance
        # else:
        #     for photo_obj in photo_data:
        #         photo_fields = dict(photo_obj)
        #         image = ImageGalery.objects.create(**photo_fields)
        #         image.save()
        #         instance.image_field.add(image)
        instance.save()

        return instance
    

    def validate(self, data):
        current_house = data['house']
        if current_house.accomodation.filter(number=data['number']).exists() and\
                current_house.accomodation.filter(number=data['number'])[0].id != self.instance.id:
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
    


class AdsAccomodationRetreaveSerializer(serializers.ModelSerializer):
    floor_quantity = serializers.SerializerMethodField()
    floor_title = serializers.SerializerMethodField()
    house_address = serializers.SerializerMethodField()
    house_disctrict = serializers.SerializerMethodField()
    house_type = serializers.SerializerMethodField()
    type_of_account = serializers.SerializerMethodField()
    builder_data = serializers.SerializerMethodField()

    class Meta:
        model = Accomodation
        fields = ['planing', 'area', 'floor_title', 'floor_quantity',\
                'house_address', 'house_disctrict', 'image_field',
                'type_status', 'house_type', 'planing',\
                'area_kitchen', 'heat_type', 'have_balcony',\
                'type_of_account', 'builder_data']
        depth = 1

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
    
    def get_house_type(self, obj):
        house_type=obj.house.house_type
        return house_type

    def get_type_of_account(self, obj):
        type_of_account=obj.house.type_of_account
        return type_of_account
    
    def get_builder_data(self, obj):

        # try:
        #     builder_data={'email': obj.house.builder.email,
        #                 'image': obj.house.builder.photo}
        # except ValueError:
        #     builder_data={'email': obj.house.builder.email}
        
        builder_data={'email': obj.house.builder.email}
        return builder_data
    
    
class AdsAccomodationDataListSerializer(AdsAccomodationRetreaveSerializer):
    class Meta:
        model = Accomodation
        fields = ['planing', 'area', 'floor_title', 'floor_quantity',\
                'house_address', 'house_disctrict', 'image_field',\
                'ads_status']
        depth = 1    


class AdsListModerationSerializer(serializers.ModelSerializer):
    accomodation = AdsAccomodationDataListSerializer(many=False, required=False)

    class Meta:
        model = Ads
        fields = ['id', 'cost', 'accomodation', 'version_of_calculation',\
                  'date_added', 'ads_status']




class AdsRetreaveModerationSerializer(serializers.ModelSerializer):
    accomodation = AdsAccomodationRetreaveSerializer(many=False, required=False)

    class Meta:
        model = Ads
        fields = ['id', 'accomodation']


class DeniedCauseSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeniedCause
        fields = ['text',]



class AdsupdateModerationSerializer(serializers.ModelSerializer):
    denied_cause=serializers.PrimaryKeyRelatedField(required=True, queryset = DeniedCause.objects.all())

    class Meta:
        model = Ads
        fields = ['id', 'denied_cause', 'ads_status']

    def validate(self, data):
            request = self.context.get("request")
            try:
                if data['denied_cause'] and data['ads_status'] == 'non_moderated' or data['ads_status'] == 'approved':
                    raise serializers.ValidationError("Причину відмови можно позначити, якщо оголошенню відмовіленно.")
            except KeyError:
                pass

            return data