from django.contrib import admin
from django.urls import path, include

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    # django urls
    path('admin/', admin.site.urls),
    # third part url`s
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    # path('api/rest-auth/', include('rest_auth.urls')),
    # path('rest-auth/registration/', include('rest_auth.registration.urls')),
    # developed url`s
    path("users/", include("users.urls")),
    # path("ads/", include("src.ads.urls")),
    path("houses/", include("houses.urls")),
]