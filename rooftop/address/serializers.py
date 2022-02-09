from rest_framework import serializers

from .models import  Roof_info, Project, Calculation
from users.models import User

# class AddressListSerializer(serializers.ModelSerializer):
#     username = serializers.SerializerMethodField(source='get_username')
#     first_name = serializers.SerializerMethodField(source='get_first_name')
#     last_name = serializers.SerializerMethodField(source='get_last_name')

#     class Meta:
#         model = Address
#         fields = ('username', 'address', 'project', 'client', 'first_name', 'last_name')

#     def get_username(self, obj):
#         return obj.user.username

#     def get_first_name(self, obj):
#         return obj.user.first_name

#     def get_last_name(self, obj):
#         return obj.user.last_name

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class RoofInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roof_info
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    calculations = serializers.SerializerMethodField(source='get_calculations')
    class Meta:
        model = Project
        fields = ('id','client', 'project_name', 'address', 'building_type', 'floors', 'task_target',\
             'consumption_overwrite', 'utility_overwrite', 'address_image','calculations',)

    def get_calculations(self, obj):
        queryset = Calculation.objects.filter(project=obj).order_by('row')
        serializer = CalculationSerializer
        return serializer(queryset, many=True).data


class CalculationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calculation
        exclude = ['project']