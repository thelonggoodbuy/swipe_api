from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication


from .serializers import HouseSerializer, HouseBuildingSerializer, \
                        HouseEntancesSerializer, FloorSerializer, \
                        RiserSerializer
from .models import House, HouseBuilding, HouseEntrance, Floor, Riser


from users.services import AdminOnlyPermission, AdminOrBuildeOwnerPermission

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated




class HouseViewSet(ModelViewSet):
    '''
    House CRUD.
    '''
    permission_classes = [IsAuthenticated, AdminOrBuildeOwnerPermission]
    authentication_classes = [JWTAuthentication]
    serializer_class = HouseSerializer
    queryset = House.objects.all()




class HouseBuildingViewSet(ModelViewSet):
    '''
    House building CRUD
    '''
    permission_classes = [IsAuthenticated, AdminOrBuildeOwnerPermission]
    authentication_classes = [JWTAuthentication]
    serializer_class = HouseBuildingSerializer
    
    def get_queryset(self):
        queryset = HouseBuilding.objects.all()
        return queryset
    

class HouseEntancesViewSet(ModelViewSet):
    '''
    House building CRUD
    '''
    permission_classes = [IsAuthenticated, AdminOrBuildeOwnerPermission]
    authentication_classes = [JWTAuthentication]
    serializer_class = HouseEntancesSerializer
    
    def get_queryset(self):
        # queryset = HouseEntrance.objects.filter(house__builder = self.request.user)
        queryset = HouseEntrance.objects.all()
        return queryset


class FloorViewSet(ModelViewSet):
    '''
    House building CRUD
    '''
    permission_classes = [IsAuthenticated, AdminOrBuildeOwnerPermission]
    authentication_classes = [JWTAuthentication]
    serializer_class = FloorSerializer
    
    def get_queryset(self):
        queryset = Floor.objects.all()
        return queryset


class RiserViewSet(ModelViewSet):
    '''
    House building CRUD
    '''
    permission_classes = [IsAuthenticated, AdminOrBuildeOwnerPermission]
    authentication_classes = [JWTAuthentication]
    serializer_class = RiserSerializer
    
    def get_queryset(self):
        queryset = Riser.objects.all()
        return queryset
