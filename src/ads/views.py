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

@extend_schema(tags=['Ads: Accomodation'])
class AccomodationViewSet(ModelViewSet):
    '''
    Accomodation CRUD and logic for working with nested images.
    '''
    permission_classes = [IsAuthenticated, AdminOrBuildeOwnerPermission]
    authentication_classes = [JWTAuthentication]
    serializer_class = AccomodationSerializer
    queryset = Accomodation.objects.all()



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
    serializer_class = AdsSerializer
    queryset = Ads.objects.all()

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
    


@extend_schema(tags=['Ads: Ads'])
class AdsPromoView(generics.UpdateAPIView):
    model = Ads
    serializer_class = AdsPromoUpdateSerializer
    permission_classes = [IsAuthenticated, AdminOrBuildeOwnerPermission]


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
class ModerationAdsViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin, UpdateModelMixin,):
    permission_classes = [AllowAny]
    authentication_classes = [JWTAuthentication]
    queryset = Ads.objects.all()
    serializer_class = AdsupdateModerationSerializer
    

    def list(self, *args, **kwargs):
        ads_list = Ads.objects.all()
        serializer = AdsListModerationSerializer(ads_list, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = AdsRetreaveModerationSerializer(instance)
        return Response(serializer.data)
    




@extend_schema(tags=['Ads: DeniedCause'])
class DeniedCauseViewSet(ModelViewSet):
    '''
    DeniedCause CRUD.
    '''
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]
    serializer_class = DeniedCauseSerializer
    queryset = DeniedCause.objects.all()





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

    @extend_schema(summary='Retreave aproved ads. Needfull permission - all authenticated users.')
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    @extend_schema(summary='Partly update for adding to favourite ads. Needfull permission - all authenticated users.')
    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.context['user'] = self.request.user
        
        if serializer.is_valid():
            serializer.save(instance, serializer.validated_data)
            if serializer.validated_data['add_to_favourite'] == True:
                response_text = f'Ви додали оголошення №{instance.id} до переліку вибранного.'
            elif serializer.validated_data['add_to_favourite'] == False:
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


    @extend_schema(summary='Partly update BOOKING fields for ACCOMODATION. Needfull permission - admin or builder.')
    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save(instance, serializer.validated_data)

        return Response({"message": 'all work!'})
    
    # @swagger_auto_schema(auto_schema=None)
    # def put(self, request, *args, **kwargs):
    #     return



# **********************************************************************
# ==============END====WORK==AREA======================================
# **********************************************************************