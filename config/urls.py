from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from rest_framework.authtoken.views import obtain_auth_token

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)



urlpatterns = [
    # django urls
    path('admin/', admin.site.urls),
    # third part url`s
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    # local urls
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path("users/", include("users.urls")),
    path("houses/", include("houses.urls")),
    path("ads/", include("ads.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)