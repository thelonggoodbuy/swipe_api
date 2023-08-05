from rest_framework import serializers
from django.db.models import Q

from drf_extra_fields.fields import Base64ImageField


from .models import House, HouseBuilding, HouseEntrance, Floor, Riser
from users.models import CustomUser


class HouseSerializer(serializers.ModelSerializer):
    builder = serializers.PrimaryKeyRelatedField\
        (queryset=CustomUser.objects.filter\
        ((Q(is_builder=True)) | Q(is_superuser=True)), required=False)
    

    class Meta:
        model = House
        fields = ['id', 'description', 'address', 'disctrict',
                  'microdisctrict', 'house_status', 'house_type',
                  'house_class', 'building_technology', 'square_type',
                  'distance_to_sea', 'services_payment', 'ceiling_height',
                  'household_gas', 'heating', 'sewage', 'plumbing', 
                  'builder', 'registration', 'type_of_account',
                  'purpose', 'summ_of_threaty', 'main_image', 'location']
        
    def validate(self, data):
        if data['house_type'] == 'коттедж' and data['house_status'] != ('індивідуальний будинок' or None):
            raise serializers.ValidationError("Коттедж може бути тільки індивідуальним будинком. А індивідуальний будинок не може містити квартири")

        return data
    


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
    