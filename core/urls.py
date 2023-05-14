from django.contrib import admin
from main.viewsets import VerifyUserAPIView
from django.urls import path, include
from .routers import router
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/', include(router.urls)),
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/verify_otp/', VerifyUserAPIView.as_view(), name='verify_otp'),
]
