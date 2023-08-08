from .views import AccomodationViewSet, AdsViewSet

from rest_framework.routers import DefaultRouter

from django.urls import path, include



# app_name = "ads"

router = DefaultRouter()
router.register(r'accomodation', AccomodationViewSet, basename='accomodation')
router.register(r'ads', AdsViewSet, basename='ads')

urlpatterns = [
    path('', include(router.urls)),
]
