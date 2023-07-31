# from .views import HouseViewSet

# from rest_framework.routers import DefaultRouter

from django.urls import path, include

from .views import UserLoginAPIView, UserRegistrationAPIView, \
                    UserDetailAndUpdateAPIView, UserChangePasswordRequestView,\
                    SimpleUserChangePasswordView, MessageCreateAndListForSimpleUser

from users.views import ActivateUser

# router = DefaultRouter()
# router.register(r'houses', HouseViewSet, basename='house')

app_name = "users"

urlpatterns = [
    path("auth/login_simple_user/", UserLoginAPIView.as_view(), name="login-simple-user"),
    path("auth/register_simple_user/", UserRegistrationAPIView.as_view(), name="register-simple-user"),
    path("auth/activate_simple_user/<uidb64>/<token>/", ActivateUser.as_view(), name='activate'),

    path("simple_user_update_and_detail/<int:pk>/", UserDetailAndUpdateAPIView.as_view(), name="simple-user-update-and-detail"),

    path("user_change_password_request/<int:pk>/", UserChangePasswordRequestView.as_view(), name="user-change-password-request"),

    path("user_change_password/<uidb64>/<token>/", SimpleUserChangePasswordView.as_view(), name='change_password'),

    path("message_create_or_list/", MessageCreateAndListForSimpleUser.as_view(), name='message-create-or-list'),

    # path("message_create_or_list/<int:pk>/", MessageCreateAndListForSimpleUser.as_view(), name='message-create-or-list'),
]
