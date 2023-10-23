from rest_framework import serializers
from django.db.models import Q

from drf_extra_fields.fields import Base64ImageField


from .models import House, HouseBuilding, HouseEntrance, Floor, Riser
from users.models import CustomUser
from ads.models import ImageGalery





class PhotoToHouseSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)

    class Meta:
        model = ImageGalery
        fields = ['id', 'image']



class ModelListField(serializers.ListField):
    

    def to_representation(self, data):
        list_data = list(data.all())
        for obj in list_data: 
            obj.name = {"id": obj.id, "image": obj.image.url}

        return [self.child.to_representation(item) if item is not None else None for item in list_data]
        # return super().to_representation(list_data)
    
    def to_internal_value(self, data):

        if data == ['']: data = []
        for image in data[:]:
            if image == 'string': data.remove(image)
        return super().to_internal_value(data)



class HouseSerializer(serializers.ModelSerializer):
    builder = serializers.PrimaryKeyRelatedField\
        (queryset=CustomUser.objects.filter\
        ((Q(is_builder=True)) | Q(is_superuser=True)), required=False)
    image_field = ModelListField(required=False, allow_null=True, child=serializers.ImageField(max_length=100000, allow_empty_file=False, use_url=False))

    class Meta:
        model = House
        fields = ['id', 'description', 'address', 'disctrict',
                  'microdisctrict', 'house_status', 'house_type',
                  'house_class', 'building_technology', 'square_type',
                  'distance_to_sea', 'services_payment', 'ceiling_height',
                  'household_gas', 'heating', 'sewage', 'plumbing', 
                  'builder', 'registration', 'type_of_account',
                  'purpose', 'summ_of_threaty', 'main_image', 'image_field']
        extra_kwargs = {'house_type': {'required': False}}


    def create(self, validated_data):
        images_data = []
        if 'image_field' in validated_data:
            images_data = validated_data.pop('image_field')
        house = House.objects.create(**validated_data)
        image_new_data = [ImageGalery(image=obj) for obj in images_data]
        image_obj_list = ImageGalery.objects.bulk_create(image_new_data)
        house.image_field.set(image_obj_list)
        return house


    def update(self, instance, validated_data):

        if 'image_field' in validated_data and validated_data['image_field'] != []:
            photo_data = validated_data.pop('image_field')

        for item in validated_data:
            if House._meta.get_field(item) and validated_data[item] not in ['', None, []]:
                setattr(instance, item, validated_data[item])

        try:
            photo_data
        except NameError:
            instance.save()
            return instance
        else:
            if photo_data != []:
                image_new_data = [ImageGalery(image=obj) for obj in photo_data]
                image_obj_list = ImageGalery.objects.bulk_create(image_new_data)
            else:
                # print('-----!!!--------')
                ImageGalery.objects.filter(house=instance).delete()
                image_obj_list = []
            
            instance.image_field.set(image_obj_list)
        instance.save()
        return instance


    def validate_builder(self, data):
        if data == self.context.get("request").user.id or self.context.get("request").user.is_superuser == True:
            return data
        else:
            raise serializers.ValidationError("Тільки адміністратор має можливість змінювати данні про власнітьс об'єкта нерухомості.")

    def validate(self, data):
        print(data)
        if 'house_type'in data:
            if data['house_type'] == 'коттедж' and data['house_status'] != ('індивідуальний будинок' or None):
                raise serializers.ValidationError("Коттедж може бути тільки індивідуальним будинком. А індивідуальний будинок не може містити квартири")

        return data
    

class HouseListSerializer(HouseSerializer):
    image_field = PhotoToHouseSerializer(many=True, read_only=True)


class HouseBuildingSerializer(serializers.ModelSerializer):
    house = serializers.PrimaryKeyRelatedField(required=True, queryset = House.objects.all())


    class Meta:
        model = HouseBuilding
        fields = ['id', 'house', 'title']

    def validate(self, data):
        request = self.context.get("request")
        if (data['house'] not in House.objects.filter(builder=request.user)) and request.user.is_superuser == False:
            raise serializers.ValidationError("Змінювати такий тип данних може тільки забудовник, або адмін.")

        return data
    


class HouseEntancesSerializer(serializers.ModelSerializer):
    house = serializers.PrimaryKeyRelatedField(required=True, queryset = House.objects.all())


    class Meta:
        model = HouseEntrance
        fields = ['id', 'house', 'title']

    def validate(self, data):
        request = self.context.get("request")
        if (data['house'] not in House.objects.filter(builder=request.user)) and request.user.is_superuser == False:
            raise serializers.ValidationError("Змінювати такий тип данних може тільки забудовник, або адмін.")

        return data
    

class FloorSerializer(serializers.ModelSerializer):
    house = serializers.PrimaryKeyRelatedField(required=True, queryset = House.objects.all())
    floor_schema = Base64ImageField(required=False)

    class Meta:
        model = Floor
        fields = ['id', 'house', 'title', 'floor_schema']

    def validate(self, data):
        request = self.context.get("request")
        if (data['house'] not in House.objects.filter(builder=request.user)) and request.user.is_superuser == False:
            raise serializers.ValidationError("Змінювати такий тип данних може тільки забудовник, або адмін.")

        return data
    

class RiserSerializer(serializers.ModelSerializer):
    house = serializers.PrimaryKeyRelatedField(required=True, queryset = House.objects.all())

    class Meta:
        model = Riser
        fields = ['id', 'house', 'title']

    def validate(self, data):
        request = self.context.get("request")
        if (data['house'] not in House.objects.filter(builder=request.user)) and request.user.is_superuser == False:
            raise serializers.ValidationError("Змінювати такий тип данних може тільки забудовник, або адмін.")

        return data
    