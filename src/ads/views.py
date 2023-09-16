from django.db.models import Q
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import action
from rest_framework.settings import api_settings
from rest_framework import serializers
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, UpdateModelMixin, RetrieveModelMixin

from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend


from rest_framework.views import APIView


from .serializers import AccomodationSerializer, PhotoToAccomodationSerializer,\
                            AdsSerializer, DeniedCauseSerializer, \
                            AdsListModerationSerializer, AdsRetreaveModerationSerializer,\
                            AdsupdateModerationSerializer, AdsFeedListSerializer,\
                            AdsRetreaveUpdateFavouritesSerializer, AdsListFavouritesSerializer,\
                            AdsPromoUpdateSerializer, AdsListChessboardSerializer, BookedAccomodationSerializer

from .models import Accomodation, ImageGalery, Ads, DeniedCause
from houses.models import House

from users.services import AdminOrBuildeOwnerPermission


# =============================================================================================
# ==================ACCOMODATION====LOGIC======================================================
# =============================================================================================
from rest_framework.parsers import JSONParser, MultiPartParser

@extend_schema(tags=['Ads: Accomodation'])
# @extend_schema_view(put=extend_schema(exclude=True))
class AccomodationViewSet(ModelViewSet):
    '''
    Accomodation CRUD and logic for working with nested images.
    '''
    permission_classes = [IsAuthenticated, AdminOrBuildeOwnerPermission]
    authentication_classes = [JWTAuthentication]
    serializer_class = AccomodationSerializer
    queryset = Accomodation.objects.all()
    parser_classes = [JSONParser]


    def get_queryset(self):
        queryset = Accomodation.objects.prefetch_related('image_field').select_related('house__builder', 'booked_by')
        return queryset
    
    @extend_schema(summary='Get list (LIST) of all accomodation(in owning - for BUILDER and total - for ADMIN). Needfull permission - admin or builder')
    def list(self, request, *args, **kwargs):

        if self.request.user.is_superuser == True:
            queryset = Accomodation.objects.all().\
                prefetch_related('image_field')
        else:
            queryset =  Accomodation.objects.filter(house__builder=self.request.user)\
                .prefetch_related('image_field')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)



    @extend_schema(summary='Create accomodation (CREATE). Needfull permission - admin or builder')
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(summary='Retreave accomodation (RETREAVE). Needfull permission - admin or builder.')
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @extend_schema(summary='Update accomodation (PUT). Needfull permission - admin or builder(Partial change house, builded by user).')    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        return Response(serializer.data)


    @extend_schema(summary='Partial update accomodation (PATCH). Needfull permission - admin or builder(Partial change house, builded by user).')
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(summary='Delete accomodation. Needfull permission - admin or builder.')
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

# =============================================================================================
# ===========================ADS====LOGIC======================================================
# =============================================================================================



@extend_schema(tags=['Ads: Ads'])
class AdsViewSet(ModelViewSet):
    '''
    Ads CRUD and logic for working with ADS.
    '''
    permission_classes = [IsAuthenticated, AdminOrBuildeOwnerPermission]
    authentication_classes = [JWTAuthentication]
    parser_classes = [JSONParser]
    serializer_class = AdsSerializer
    queryset = Ads.objects.all()

    @extend_schema(summary='Return LIST of ads. Needfull permission - admin or builder')
    def list(self, request, *args, **kwargs):
        if self.request.user.is_superuser == True:
            queryset = Ads.objects.all()
        else:
            queryset = Ads.objects.filter(accomodation__house__builder=self.request.user)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @extend_schema(summary='RETREAVE ads object. Needfull permission - admin or builder')
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(summary='CREATE ads object. Needfull permission - admin or builder')
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @extend_schema(summary='UPDATE ads object. Needfull permission - admin or builder')
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @extend_schema(summary='PARTIAL UPDATE ads object. Needfull permission - admin or builder')
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @extend_schema(summary='DELETE ads object. Needfull permission - admin or builder')
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    


@extend_schema(tags=['Ads: Ads'])
@extend_schema_view(put=extend_schema(exclude=True))
class AdsPromoView(generics.UpdateAPIView):
    model = Ads
    serializer_class = AdsPromoUpdateSerializer
    permission_classes = [IsAuthenticated, AdminOrBuildeOwnerPermission]
    parser_classes = [MultiPartParser]


    def get_queryset(self):
        queryset = Ads.objects\
            .select_related('accomodation', 'accomodation__floor')\
            .prefetch_related('accomodation__image_field', 'accomodation__house__floor', 'favorites_for')\
            .filter(ads_status='approved')
        return queryset


    @extend_schema(summary='Partly update promo fields for Ads. Needfull permission - admin or builder.')
    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save(instance, serializer.validated_data)

        return Response({"message": 'all work!'})



@extend_schema(tags=['Ads: Ads moderation'])
@extend_schema_view(update=extend_schema(exclude=True))
class ModerationAdsViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin, UpdateModelMixin,):
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]
    queryset = Ads.objects.all()
    serializer_class = AdsupdateModerationSerializer
    
    @extend_schema(summary='List of all Ads - aproved and not approved. Needfull permission - admin.')
    def list(self, *args, **kwargs):
        ads_list = Ads.objects.all().order_by("-id").order_by("-ads_status")
        serializer = AdsListModerationSerializer(ads_list, many=True)
        return Response(serializer.data)
    
    @extend_schema(summary='Retreve of single Ads. Needfull permission - admin.')
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = AdsRetreaveModerationSerializer(instance)
        return Response(serializer.data)
    
    @extend_schema(summary='Partial update and approve of single Ads. Needfull permission - admin.')
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)



@extend_schema(tags=['Ads: DeniedCause'])
class DeniedCauseViewSet(ModelViewSet):
    '''
    DeniedCause CRUD.
    '''
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]
    serializer_class = DeniedCauseSerializer
    queryset = DeniedCause.objects.all()

    @extend_schema(summary='List denied cause object. Needfull permission - admin')
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @extend_schema(summary='Create denied cause object. Needfull permission - admin')
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(summary='Retreave denied cause object. Needfull permission - admin')
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @extend_schema(summary='Update denied cause object. Needfull permission - admin')
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @extend_schema(summary='Partly Update denied cause object. Needfull permission - admin')
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @extend_schema(summary='Delete denied cause object. Needfull permission - admin')
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)



# =============================================================================================
# ==================ADS====LINE====LOGIC=======================================================
# =============================================================================================

@extend_schema(tags=['Ads: Ads'])
class AdsFeedListView(generics.ListAPIView):
    model = Ads
    serializer_class = AdsFeedListSerializer
    permission_classes = [IsAuthenticated]


    def get_queryset(self):
        queryset = Ads.objects\
            .select_related('accomodation', 'accomodation__floor')\
            .prefetch_related('accomodation__image_field', 'accomodation__house__floor')\
            .filter(ads_status='approved')
        return queryset


    @extend_schema(summary='Get list of approved ADS. Needfull permission - all authenticated users.')
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    

    @extend_schema(summary='Get list of FILTERED approved ADS. Needfull permission - all authenticated users.')
    def post(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        serializer = self.get_serializer(queryset, many=True)
        serializer.context['user'] = self.request.user
        data = []
        for ads in serializer.data:
            if ads != None: data.append(ads)
        return Response(data)




@extend_schema(tags=['Ads: Ads'])
@extend_schema_view(put=extend_schema(exclude=True))
class AdsRetreaveUpdateFavouritesView(generics.RetrieveUpdateAPIView):
    model = Ads
    serializer_class = AdsRetreaveUpdateFavouritesSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Ads.objects\
            .select_related('accomodation', 'accomodation__floor')\
            .prefetch_related('accomodation__image_field', 'accomodation__house__floor')\
            .filter(ads_status='approved')
        return queryset

    @extend_schema(summary='Retreave LIST of aproved ads. Needfull permission - all authenticated users.')
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    @extend_schema(summary='Partly update for adding to favourite ads. Needfull permission - all authenticated users.')
    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.context['user'] = self.request.user
        
        if serializer.is_valid():
            serializer.save(instance, serializer.validated_data)
            if 'add_to_favourite' in serializer.validated_data and serializer.validated_data['add_to_favourite'] == True:
                response_text = f'Ви додали оголошення №{instance.id} до переліку вибранного.'
            elif 'add_to_favourite' in serializer.validated_data and serializer.validated_data['add_to_favourite'] == False:
                response_text = f'Ви видалили оголошення №{instance.id} з переліку вибранного.'
            else:
                response_text = f'Ви не здійснили жодних змін в переліку вибранного.'
            return Response({"message": response_text})
        else:
            return Response({"message": "failed", "details": serializer.errors})
        


@extend_schema(tags=['Ads: Ads'])
class AdsListFavouritesView(generics.ListAPIView):
    model = Ads
    serializer_class = AdsListFavouritesSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        Q_list = []
        Q_list.append(Q(ads_status='approved'))
        queryset = self.request.user.favourites_adds\
            .select_related('accomodation', 'accomodation__floor')\
            .prefetch_related('accomodation__image_field', 'accomodation__house__floor')\
            .filter(*Q_list)
        return queryset

    @extend_schema(summary='Get list of USER FAVOURITES ads. Needfull permission - all authenticated users.')
    def get(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    

@extend_schema(tags=['Ads: Chessboard'])
class AdsListChessboardView(generics.RetrieveAPIView):
    model = House
    serializer_class = AdsListChessboardSerializer
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser]


    def get_queryset(self):
        queryset = House.objects.all()
        return queryset

    @extend_schema(summary='Get CHESSBOARD of ads. Needfull permission - all authenticated users.')
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @extend_schema(summary='Get CHESSBOARD WITH FILTERS of ads. Needfull permission - all authenticated users.')
    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        serializer.filter_chessboard(serializer)
        return Response(serializer.data)


# **********************************************************************
# ======================WORK==AREA======================================
# **********************************************************************

@extend_schema(tags=['Ads: Accomodation'])
@extend_schema_view(put=extend_schema(exclude=True))
class BookedAccomodationView(generics.UpdateAPIView):
    model = Accomodation
    serializer_class = BookedAccomodationSerializer
    permission_classes = [AllowAny]
    queryset = Accomodation.objects.all()
    parser_classes = [MultiPartParser]


    @extend_schema(summary='Partly update BOOKING fields for ACCOMODATION. Needfull permission - admin or builder.')
    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save(instance, serializer.validated_data)

        return Response({"message": 'all work!'})

# **********************************************************************
# ==============END====WORK==AREA======================================
# **********************************************************************