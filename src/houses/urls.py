from .views import HouseViewSet, HouseBuildingViewSet,\
                     HouseEntancesViewSet, FloorViewSet,\
                     RiserViewSet

from rest_framework.routers import DefaultRouter

from django.urls import path, include




router = DefaultRouter()
router.register(r'houses', HouseViewSet, basename='house')
router.register(r'houses_building', HouseBuildingViewSet, basename='houses_building')
router.register(r'house_entrance', HouseEntancesViewSet, basename='house_entrance')
router.register(r'house_floor', FloorViewSet, basename='house_floor')
router.register(r'house_riser', RiserViewSet, basename='house_riser')

urlpatterns = [
    path('', include(router.urls)),
]
