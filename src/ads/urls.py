from .views import AccomodationViewSet, AdsViewSet, DeniedCauseViewSet,\
                    ModerationAdsViewSet, AdsFeedListView, AdsRetreaveUpdateFavouritesView,\
                    AdsListFavouritesView, AdsPromoView

from rest_framework.routers import DefaultRouter

from django.urls import path, include



# app_name = "ads"

router = DefaultRouter()
router.register(r'accomodation', AccomodationViewSet, basename='accomodation')
router.register(r'ads', AdsViewSet, basename='ads')
router.register(r'denied_cause', DeniedCauseViewSet, basename='denied_cause')
router.register(r'moderation_ads', ModerationAdsViewSet, basename='moderation_ads')


urlpatterns = [
    path("", include(router.urls)),
    path("ads-feed/", AdsFeedListView.as_view(), name='ads_feed'),
    path("ads_retreave_or_add_to_favourite/<int:pk>/", AdsRetreaveUpdateFavouritesView.as_view(), name='ads_retreave_or_add_to_favourite'),
    path("ads_list_favourites/", AdsListFavouritesView.as_view(), name='ads_list_favourites'),    
    path("ads_promo_update/<int:pk>", AdsPromoView.as_view(), name='ads_promo_update'),
]
