from rest_framework import serializers


from .models import Accomodation, ImageGalery, Ads, DeniedCause, Filter, PromoAdditionalPhrase

from drf_spectacular.utils import extend_schema_serializer, OpenApiExample

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

            for dict_of_image_id in list_of_dict_images_id: list_of_images_id.append(dict_of_image_id['id'])

            for image_obj in validated_data['image_field']:
                
                # delete if order None
                if 'obj_order' not in image_obj:
                    delete_obj = image_obj['id']
                    # deleted_list.append(delete_obj)
                    image_obj = ImageGalery.objects.get(id=image_obj['id'])
                    instance.image_field.remove(image_obj)
                    del image_obj
                # update image
                elif 'id' in image_obj and image_obj['id'] in list_of_images_id:
                    ImageGalery.objects.filter(id=image_obj['id']).update(**image_obj)
                # create image
                else:

                    new_image = ImageGalery.objects.create(**image_obj)
                    instance.image_field.add(new_image)

        instance.save()

        return instance
    

    # def validate(self, data):
    #     current_house = data['house']
    #     if current_house.accomodation.filter(number=data['number']).exists() and\
    #             current_house.accomodation.filter(number=data['number'])[0].id != self.instance.id:
    #         raise serializers.ValidationError("Номер квартири має бути унікальним для цього будинку. Квартира з таким номером вже зареєстрована")
    #     if data['house_building'] not in current_house.house_building.all():
    #         raise serializers.ValidationError("Ви повинні обрати корпус, який знаходиться в цьому будинку.")
    #     if data['house_entrance'] not in current_house.house_entrance.all():
    #         raise serializers.ValidationError("Ви повинні обрати підїзд, який знаходиться в цьому будинку.")
    #     if data['floor'] not in current_house.floor.all():
    #         raise serializers.ValidationError("Ви повинні обрати поверх, який знаходиться в цьому будинку.")
    #     if data['riser'] not in current_house.riser.all():
    #         raise serializers.ValidationError("Ви повинні обрати стояк, який знаходиться в цьому будинку.")

    #     return data
    


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
    

# =======================================================================================
# ==========CUSTOM===FILTERS=====SERIALIZERS=============================================
# =======================================================================================

@extend_schema_serializer(exclude_fields=('cost',),
                          examples = [
                                OpenApiExample(
                                    'Title. Title.',
                                    summary='Filter values',
                                    description='Simple values.',
                                    value={
                                        'filter_from_cost': '',
                                        'filter_to_cost': '',
                                        'filter_type_status': '',
                                        'filter_disctrict': ''
                                    },
                                    request_only=True,
                                ),
                                    ])
class AdsFeedListSerializer(serializers.ModelSerializer):
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
        ('new_building', 'новобудова'),
        ('cottage', 'коттедж')
    )

    EXISTING_FILTERS = ([saved_filter.id for  saved_filter in Filter.objects.all()])

    accomodation_data = serializers.SerializerMethodField()

    filter_from_cost = serializers.IntegerField(required=False)
    filter_to_cost = serializers.IntegerField(required=False)
    filter_type_status = serializers.ChoiceField(required=False, choices=TYPE_CORT)
    filter_disctrict = serializers.CharField(required=False)
    filter_microdisctrict = serializers.CharField(required=False)
    filter_from_area = serializers.CharField(required=False)
    filter_to_area = serializers.CharField(required=False)
    filter_house_status = serializers.ChoiceField(required=False, choices=HOUSE_STATUS_CORT)
    filter_living_condition = serializers.ChoiceField(required=False, choices=LIVING_CONDITION_CORT)
    filter_type = serializers.ChoiceField(required=False, choices=FILTER_TYPE_CORT)
    existing_filter = serializers.ChoiceField(required=False, choices=EXISTING_FILTERS)
    save_current_filter = serializers.BooleanField(required=False)

    class Meta:
        model = Ads
        fields = ['id', 'cost', 'accomodation_data', 'date_added', 'filter_from_cost', 'filter_to_cost',
                  'filter_type_status', 'filter_disctrict', 'filter_microdisctrict',
                  'filter_from_area', 'filter_to_area', 'filter_house_status', 'filter_living_condition',
                  'filter_type', 'existing_filter', 'save_current_filter']


    def get_accomodation_data(self, obj):
        accomodation_data = obj.accomodation
        data = {'planing': accomodation_data.planing,
                'area': accomodation_data.area,
                'floor': accomodation_data.floor.title,
                'total_floors': accomodation_data.house.floor.all().count(),
                'district': accomodation_data.house.disctrict,
                'address': accomodation_data.house.address,
                'location_x': accomodation_data.house.location_x,
                'location_y': accomodation_data.house.location_y,}
        
        if accomodation_data.image_field.all(): 
            image = accomodation_data.image_field.all().first()
            data['main_image'] = image.image.url
        return data
    

    def to_representation(self, obj):
            # check what filter values we use or use saved filter
            if self.context['request'].data.get('existing_filter'):
                choosen_filter_id = self.context['request'].data.get('existing_filter')
                choosen_filter = Filter.objects.filter(id = choosen_filter_id).values(
                    'filter_type_status', 'filter_disctrict', 'filter_microdisctrict',
                    'filter_from_cost', 'filter_to_cost', 'filter_from_area', 'filter_to_area',
                    'filter_living_condition'
                )
                filter_dict = {}
                for key in choosen_filter[0].keys():
                    if choosen_filter[0][key] != None and choosen_filter[0][key] != '': filter_dict[key] = choosen_filter[0][key]
            else:    
                filter_dict = self.get_filter_from_cost(obj)

            # filters saving
            if self.context['request'].data.get('save_current_filter') == 'true':
                try:
                    Filter.objects.get(user=self.context['user'], **filter_dict)
                except Filter.DoesNotExist:
                    Filter.objects.create(user=self.context['user'], **filter_dict)
                

            list_of_fields_check = []

            if len(filter_dict) == 0:
                return super(AdsFeedListSerializer, self).to_representation(obj)
            
            if 'filter_type_status' in filter_dict:
                if filter_dict['filter_type_status'] == obj.accomodation.type_status:
                    list_of_fields_check.append(True)
                else:
                    list_of_fields_check.append(False)

            if 'filter_disctrict' in filter_dict:
                if filter_dict['filter_disctrict'] == obj.accomodation.house.disctrict:
                    list_of_fields_check.append(True)
                else:
                    list_of_fields_check.append(False)

            if 'filter_microdisctrict' in filter_dict:
                if filter_dict['filter_microdisctrict'] == obj.accomodation.house.microdisctrict:
                    list_of_fields_check.append(True)
                else:
                    list_of_fields_check.append(False)

            if 'filter_from_cost' in filter_dict:
                if float(filter_dict['filter_from_cost']) < obj.cost:
                    list_of_fields_check.append(True)
                else:
                    list_of_fields_check.append(False)

            if 'filter_to_cost' in filter_dict:
                if float(filter_dict['filter_to_cost']) > obj.cost:
                    list_of_fields_check.append(True)
                else:
                    list_of_fields_check.append(False)

            if 'filter_from_area' in filter_dict:
                if float(filter_dict['filter_from_area']) < obj.accomodation.area:
                    list_of_fields_check.append(True)
                else:
                    list_of_fields_check.append(False)

            if 'filter_to_area' in filter_dict:
                if float(filter_dict['filter_to_area']) > obj.accomodation.area:
                    list_of_fields_check.append(True)
                else:
                    list_of_fields_check.append(False)

            if 'filter_house_status' in filter_dict:
                if filter_dict['filter_house_status'] == obj.accomodation.house.house_status:
                    list_of_fields_check.append(True)
                else:
                    list_of_fields_check.append(False)

            if 'filter_living_condition' in filter_dict:
                if filter_dict['filter_living_condition'] == obj.accomodation.living_condition:
                    list_of_fields_check.append(True)
                else:
                    list_of_fields_check.append(False)

            if 'filter_type' in filter_dict:
                if filter_dict['filter_type'] == obj.accomodation.type_status or filter_dict['filter_type'] == 'all':
                    list_of_fields_check.append(True)
                else:
                    list_of_fields_check.append(False)

            if all(list_of_fields_check):
                return super(AdsFeedListSerializer, self).to_representation(obj)



    def get_filter_from_cost(self, obj):

        filter_dict = {}

        if self.context['request'].data.get('filter_type_status'):
            filter_dict['filter_type_status'] = self.context['request'].data.get('filter_type_status')

        if self.context['request'].data.get('filter_disctrict'):
            filter_dict['filter_disctrict'] = self.context['request'].data.get('filter_disctrict')

        if self.context['request'].data.get('filter_microdisctrict'):
            filter_dict['filter_microdisctrict'] = self.context['request'].data.get('filter_microdisctrict')

        if self.context['request'].data.get('filter_from_cost'):
            filter_dict['filter_from_cost'] = self.context['request'].data.get('filter_from_cost')

        if self.context['request'].data.get('filter_to_cost'):
            filter_dict['filter_to_cost'] = self.context['request'].data.get('filter_to_cost')

        if self.context['request'].data.get('filter_from_area'):
            filter_dict['filter_from_area'] = self.context['request'].data.get('filter_from_area')

        if self.context['request'].data.get('filter_to_area'):
            filter_dict['filter_to_area'] = self.context['request'].data.get('filter_to_area')

        if self.context['request'].data.get('filter_house_status'):
            filter_dict['filter_house_status'] = self.context['request'].data.get('filter_house_status')

        if self.context['request'].data.get('filter_living_condition'):
            filter_dict['filter_living_condition'] = self.context['request'].data.get('filter_living_condition')

        if self.context['request'].data.get('filter_type'):
            filter_dict['filter_type'] = self.context['request'].data.get('filter_type')

        return filter_dict
    



    
class AdsRetreaveUpdateFavouritesSerializer(serializers.ModelSerializer):

    accomodation_data = serializers.SerializerMethodField()
    add_to_favourite = serializers.BooleanField(required=False, default=False)

    class Meta:
        model = Ads
        fields = ['id', 'cost', 'cost_per_metter', 'accomodation_data', 'date_added',
                  'agent_commission', 'cost_per_metter', 'add_to_favourite']
        read_only_fields = ['id', 'cost', 'cost_per_metter', 'accomodation_data', 'date_added',
                            'agent_commission', 'cost_per_metter']        

    def get_accomodation_data(self, obj):
        accomodation_data = obj.accomodation
        data = {'planing': accomodation_data.planing,
                'area': accomodation_data.area,
                'floor': accomodation_data.floor.title,
                'total_floors': accomodation_data.house.floor.all().count(),
                'district': accomodation_data.house.disctrict,
                'address': accomodation_data.house.address,
                'location_x': accomodation_data.house.location_x,
                'location_y': accomodation_data.house.location_y,}
        
        if accomodation_data.image_field.all(): 
            image = accomodation_data.image_field.all().first()
            data['main_image'] = image.image.url
        return data
    
    def save(self, instance, validated_data):
        if validated_data.get('add_to_favourite') == True:
            instance.favorites_for.add(self.context['user'])
            instance.save()
        elif validated_data.get('add_to_favourite') == False and\
                instance.favorites_for !=None and\
                instance.favorites_for.all().filter(id=self.context['user'].id):
            instance.favorites_for.remove(self.context['user'])
            instance.save()
        else:
            pass
        return instance
    


class AdsListFavouritesSerializer(serializers.ModelSerializer):
    accomodation_data = serializers.SerializerMethodField()

    class Meta:
        model = Ads
        fields = ['id', 'cost', 'accomodation_data', 'date_added']

    def get_accomodation_data(self, obj):
        accomodation_data = obj.accomodation
        data = {'planing': accomodation_data.planing,
                'area': accomodation_data.area,
                'floor': accomodation_data.floor.title,
                'total_floors': accomodation_data.house.floor.all().count(),
                'district': accomodation_data.house.disctrict,
                'address': accomodation_data.house.address,
                'location_x': accomodation_data.house.location_x,
                'location_y': accomodation_data.house.location_y,}
        
        if accomodation_data.image_field.all(): 
            image = accomodation_data.image_field.all().first()
            data['main_image'] = image.image.url
        return data
    


# class PromoAdditionalPhrasesSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PromoAdditionalPhrase
#         fields = ['id', 'text']



class AdsPromoUpdateSerializer(serializers.ModelSerializer):

    EXISTING_PROMO_PHRASES = ([(saved_filter.id, saved_filter.text) for saved_filter in PromoAdditionalPhrase.objects.all()])

    promotion_additional_phrase = serializers.ChoiceField(required=False, choices=EXISTING_PROMO_PHRASES)


    class Meta:
        model = Ads
        fields = ['id', 'promotion_additional_phrase', 'promotion_color_boost',
                  'is_bigger', 'is_lifted_in_feed', 'is_turbo']
        
    
    def save(self, instance, validated_data):
        if validated_data.get('promotion_additional_phrase'):
            promotion_phrase_id = validated_data.pop('promotion_additional_phrase')
            promo_text = PromoAdditionalPhrase.objects.get(id=promotion_phrase_id)
            instance.promotion_additional_phrase = promo_text

        return Ads.objects.filter(id=instance.id).update(**validated_data)
        # return instance