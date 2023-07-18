from django.contrib.auth.models import User
from rest_framework import serializers


from .models import House
# from houses.models import User



class HouseSerializer(serializers.ModelSerializer):
    sales_department = serializers.PrimaryKeyRelatedField(many=True, queryset=House.objects.all(), required=False)

    class Meta:
        model = House
        fields = ['id', 'description', 'address', 'disctrict',
                  'microdisctrict', 'house_status', 'house_type',
                  'house_class', 'building_technology', 'square_type',
                  'distance_to_sea', 'services_payment', 'ceiling_height',
                  'household_gas', 'heating', 'sewage', 'plumbing', 
                  'sales_department', 'registration', 'type_of_account',
                  'purpose', 'summ_of_threaty', 'main_image', 'location']
        
    def validate(self, data):
        if data['house_type'] == 'коттедж' and data['house_status'] != ('індивідуальний будинок' or None):
            raise serializers.ValidationError("Коттедж може бути тільки індивідуальним будинком. А індивідуальний будинок не може містити квартири")

        return data