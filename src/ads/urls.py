from .views import AccomodationViewSet, AdsViewSet, DeniedCauseViewSet, ModerationAdsViewSet, AdsFeedListView

from rest_framework.routers import DefaultRouter

from django.urls import path, include



# app_name = "ads"

router = DefaultRouter()
router.register(r'accomodation', AccomodationViewSet, basename='accomodation')
router.register(r'ads', AdsViewSet, basename='ads')
router.register(r'denied_cause', DeniedCauseViewSet, basename='denied_cause')
router.register(r'moderation_ads', ModerationAdsViewSet, basename='moderation_ads')


urlpatterns = [
    # path("moderation-ads/", ModerationAdsView.as_view(), name='moderation_ads'),
    # path("moderation-ads/<int:pk>/", ModerationAdsView.as_view(), name='moderation_ads'),
    path("", include(router.urls)),
    path("ads-feed/", AdsFeedListView.as_view(), name='ads_feed'),
    
]
