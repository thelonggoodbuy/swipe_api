from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication


from .serializers import HouseSerializer, HouseBuildingSerializer, \
                        HouseEntancesSerializer, FloorSerializer, \
                        RiserSerializer, HouseListSerializer
from .models import House, HouseBuilding, HouseEntrance, Floor, Riser


from users.services import AdminOnlyPermission, AdminOrBuildeOwnerPermission

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny

from drf_spectacular.utils import extend_schema



from rest_framework.response import Response
from rest_framework.parsers import JSONParser, MultiPartParser, FileUploadParser



@extend_schema(tags=['Houses: House'])
class HouseViewSet(ModelViewSet):
    '''
    House CRUD.
    '''
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, AdminOrBuildeOwnerPermission]
    parser_classes = [MultiPartParser]
    serializer_class = HouseSerializer
    # queryset = House.objects.select_related('image_field').filter()

    def get_queryset(self):
        print('------------GET-----QUERYSET--------')
        queryset = House.objects.prefetch_related('image_field').select_related('builder')
        return queryset
    
    @extend_schema(summary='Get list (LIST) of all buidings. Needfull permission - admin(return all houses) or builder(return houses, builded by user)')
    def list(self, request, *args, **kwargs):

        if self.request.user.is_superuser == True:
            queryset = House.objects.all().\
                prefetch_related('image_field')
        else:
            queryset =  House.objects.filter(builder=self.request.user)\
                .prefetch_related('image_field')
                # .select_related('builder')


        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    


    @extend_schema(summary='(T)Create house (CREATE). Needfull permission - admin or builder')
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(summary='(T)Retreave house (RETREAVE). Needfull permission - admin or builder(return house, builded by user).')
    def retrieve(self, request, *args, **kwargs):

        return super().retrieve(request, *args, **kwargs)
    
    @extend_schema(summary='(T)Update house (UPDATE). Needfull permission - admin or builder(change house, builded by user).')
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @extend_schema(summary='(T)Partial update house (PATCH). Needfull permission - admin or builder(Partial change house, builded by user).')
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(summary='(T)Delete house (DELETE). Needfull permission - admin or builder(delete house, builded by user).')
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)



@extend_schema(tags=['Houses: HouseBuilding'])
class HouseBuildingViewSet(ModelViewSet):
    '''
    House building CRUD
    '''

    permission_classes = [IsAuthenticated, AdminOrBuildeOwnerPermission]
    authentication_classes = [JWTAuthentication]
    serializer_class = HouseBuildingSerializer
    queryset = HouseBuilding.objects.all()
    
    @extend_schema(summary='Get list (LIST) of all house buildings. Needfull permission - admin(return all house buildings) or builder(return house buildings, builded by user)')
    def list(self, request, *args, **kwargs):

        if self.request.user.is_superuser == True:
            queryset = HouseBuilding.objects.all()
        else:
            queryset =  HouseBuilding.objects.filter(house__builder=self.request.user)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


    @extend_schema(summary='Create house building (CREATE). Needfull permission - admin or builder')
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


    @extend_schema(summary='Retreave house building (RETREAVE). Needfull permission - admin or builder(return house building, builded by user).')
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @extend_schema(summary='Update house building (UPDATE). Needfull permission - admin or builder(change house building, builded by user).')
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @extend_schema(summary='Partial update house building (PATCH). Needfull permission - admin or builder(Partial change house building, builded by user).')
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(summary='Delete house building (DELETE). Needfull permission - admin or builder(delete house building, builded by user).')
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    

@extend_schema(tags=['Houses: HouseEntrance'])
class HouseEntancesViewSet(ModelViewSet):
    '''
    House building CRUD
    '''
    permission_classes = [IsAuthenticated, AdminOrBuildeOwnerPermission]
    authentication_classes = [JWTAuthentication]
    serializer_class = HouseEntancesSerializer
    queryset = HouseEntrance.objects.all()
    
    @extend_schema(summary='Get list (LIST) of all house entrances. Needfull permission - admin(return all house entrances) or builder(return house entrances, builded by user)')
    def list(self, request, *args, **kwargs):

        if self.request.user.is_superuser == True:
            queryset = HouseEntrance.objects.all()
        else:
            queryset =  HouseEntrance.objects.filter(house__builder=self.request.user)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @extend_schema(summary='Create house entrances (CREATE). Needfull permission - admin or builder')
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


    @extend_schema(summary='Retreave house entrances (RETREAVE). Needfull permission - admin or builder(return house entrances, builded by user).')
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @extend_schema(summary='Update house entrances (UPDATE). Needfull permission - admin or builder(change house entrances, builded by user).')
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @extend_schema(summary='Partial update house entrances (PATCH). Needfull permission - admin or builder(Partial change house entrances, builded by user).')
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(summary='Delete house entrances (DELETE). Needfull permission - admin or builder(delete house entrances, builded by user).')
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


@extend_schema(tags=['Houses: Floors'])
class FloorViewSet(ModelViewSet):
    '''
    House building CRUD
    '''
    permission_classes = [IsAuthenticated, AdminOrBuildeOwnerPermission]
    authentication_classes = [JWTAuthentication]
    serializer_class = FloorSerializer
    queryset = Floor.objects.all()
    
    @extend_schema(summary='Get list (LIST) of all floors. Needfull permission - admin(return all house floors) or builder(return house floors, builded by user)')
    def list(self, request, *args, **kwargs):

        if self.request.user.is_superuser == True:
            queryset = Floor.objects.all()
        else:
            queryset =  Floor.objects.filter(house__builder=self.request.user)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @extend_schema(summary='Create floors entrances (CREATE). Needfull permission - admin or builder')
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


    @extend_schema(summary='Retreave floor (RETREAVE). Needfull permission - admin or builder(return floors, builded by user).')
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @extend_schema(summary='Update house floors (UPDATE). Needfull permission - admin or builder(change floors, builded by user).')
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @extend_schema(summary='Partial update floors (PATCH). Needfull permission - admin or builder(Partial change floors, builded by user).')
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(summary='Delete floors (DELETE). Needfull permission - admin or builder(delete floors, builded by user).')
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)



@extend_schema(tags=['Houses: Risers'])
class RiserViewSet(ModelViewSet):
    '''
    House building CRUD
    '''
    permission_classes = [IsAuthenticated, AdminOrBuildeOwnerPermission]
    authentication_classes = [JWTAuthentication]
    
    serializer_class = RiserSerializer
    queryset = Riser.objects.all()
    
    @extend_schema(summary='Get list (LIST) of all Riser. Needfull permission - admin(return all house Riser) or builder(return Riser, builded by user)')
    def list(self, request, *args, **kwargs):

        if self.request.user.is_superuser == True:
            queryset = Riser.objects.all()
        else:
            queryset =  Riser.objects.filter(house__builder=self.request.user)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @extend_schema(summary='Create risers (CREATE). Needfull permission - admin or builder')
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


    @extend_schema(summary='Retreave riser (RETREAVE). Needfull permission - admin or builder(return risers, builded by user).')
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @extend_schema(summary='Update riser (UPDATE). Needfull permission - admin or builder(change riser, builded by user).')
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @extend_schema(summary='Partial update riser (PATCH). Needfull permission - admin or builder(Partial change riser, builded by user).')
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(summary='Delete riser (DELETE). Needfull permission - admin or builder(delete floors, builded by user).')
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
