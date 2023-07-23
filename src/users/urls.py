# from .views import HouseViewSet

# from rest_framework.routers import DefaultRouter

from django.urls import path, include

from .views import UserLoginAPIView, UserLogoutAPIView, UserRegistrationAPIView


# router = DefaultRouter()
# router.register(r'houses', HouseViewSet, basename='house')

app_name = "users"

urlpatterns = [
    path("login/", UserLoginAPIView.as_view(), name="login-user"),
    path("logout/", UserLogoutAPIView.as_view(), name="logout-user"),
    path("register/", UserRegistrationAPIView.as_view(), name="register-user"),
]
