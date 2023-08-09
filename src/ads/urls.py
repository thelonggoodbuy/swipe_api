from .views import AccomodationViewSet, AdsViewSet, DeniedCauseViewSet, ModerationAdsView

from rest_framework.routers import DefaultRouter

from django.urls import path, include



# app_name = "ads"

router = DefaultRouter()
router.register(r'accomodation', AccomodationViewSet, basename='accomodation')
router.register(r'ads', AdsViewSet, basename='ads')
router.register(r'denied_cause', DeniedCauseViewSet, basename='denied_cause')


urlpatterns = [
    path("moderation-ads/", ModerationAdsView.as_view(), name='moderation_ads'),
    path("", include(router.urls))
    
]
