from django.db.models import Q
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import action
from rest_framework.settings import api_settings
from rest_framework import serializers
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, UpdateModelMixin, RetrieveModelMixin



from .serializers import AccomodationSerializer, PhotoToAccomodationSerializer,\
                            AdsSerializer, DeniedCauseSerializer, \
                            AdsListModerationSerializer, AdsRetreaveModerationSerializer,\
                            AdsupdateModerationSerializer
from .models import Accomodation, ImageGalery, Ads, DeniedCause


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

    

    
    # @action(detail=True, methods=['get'])
    # def list_of_nested_images(self, request, pk=None):
    #     current_accomodation = self.get_object()
    #     queryset = current_accomodation.image_field.all()
    #     serializer = PhotoToAccomodationSerializer(queryset, many=True)
    #     return Response(serializer.data)
        

    # @action(detail=True, methods=['post'])
    # def get_nested_image(self, request, pk=None, image_pk=None):
    #     image_list = ImageGalery.objects.filter(
    #         Q(id=request.data['id']) & Q(accomodation__id=pk))
    #     if image_list.exists():
    #         instance = image_list[0]
    #         serializer = PhotoToAccomodationSerializer(instance=instance)
    #         response = Response(serializer.data)
    #     else:
    #         raise serializers.ValidationError("Ця фотографія не прив'язана до цього обєкту нерухомості.")
    #     return response
    

    # @action(detail=True, methods=['patch'])
    # def update_nested_image(self, request, pk=None, *args, **kwargs):
    #     image_list = ImageGalery.objects.filter(
    #         Q(id=request.data['id']) & Q(accomodation__id=pk))
    #     if image_list.exists():
    #         instance = image_list[0]
    #         serializer = PhotoToAccomodationSerializer(instance=instance, data=request.data, partial=True)
    #         serializer.is_valid(raise_exception=True)
    #         self.perform_update(serializer)

    #         if getattr(instance, '_prefetched_objects_cache', None):
    #             instance._prefetched_objects_cache = {}
    #         response = Response(serializer.data)

    #     else:
    #         raise serializers.ValidationError("Ця фотографія не прив'язана до цього обєкту нерухомості.")
    #     return response
    

    # @action(detail=True, methods=['post'])
    # def create_nested_image(self, request, pk=None, *args, **kwargs):
    #     serializer = PhotoToAccomodationSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     new_image = serializer.save()
    #     current_accomodation = self.get_object()
    #     current_accomodation.image_field.add(new_image)

    #     try:
    #         headers = {'Location': str(serializer.data[api_settings.URL_FIELD_NAME])}
    #     except (TypeError, KeyError):
    #         headers = {}

    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        

    # @action(detail=True, methods=['post'])
    # def delete_nested_image(self, request, *args, **kwargs):
    #     image_instance = ImageGalery.objects.get(id=request.data['id'])
    #     image_instance.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)


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
    



from rest_framework.views import APIView



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
    
    # def update(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     print('=========UPDATE==============')
    #     print(instance)
    #     print('=========UPDATE==============')
    #     serializer = AdsupdateModerationSerializer(instance)
    #     return Response(serializer.data)




@extend_schema(tags=['Ads: DeniedCause'])
class DeniedCauseViewSet(ModelViewSet):
    '''
    DeniedCause CRUD.
    '''
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]
    serializer_class = DeniedCauseSerializer
    queryset = DeniedCause.objects.all()