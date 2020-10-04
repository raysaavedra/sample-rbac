"""capsl_test URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_auth.views import (
    LogoutView,
    PasswordChangeView,
    PasswordResetView,
    PasswordResetConfirmView,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

from boards.views import (
    accept,
    success
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("users.api.v1.urls")),
    path("api/v1/", include("boards.api.v1.urls")),
    path('api/v1/boards/<slug:board_id>/moderator-invite/<slug:user_id>/accept/', accept, name='accept'),
    path('api/v1/boards/<slug:board_id>/moderator-invite/<slug:user_id>/success/', success, name='success'),
    path('api/v1/login/', TokenObtainPairView.as_view(), name='login'),
    path('api/v1/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path("api/v1/logout/", LogoutView.as_view(), name="logout"),
    path(
        "api/v1/password_change/", PasswordChangeView.as_view(), name="password_change"
    ),
    path("api/v1/password_reset/", PasswordResetView.as_view(), name="password_reset"),
    path(
        "api/v1/password_reset/confirm/",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
]

admin.site.site_header = "capsl"
admin.site.site_title = "capsl Admin Portal"
admin.site.index_title = "capsl Admin"

# swagger
api_info = openapi.Info(
    title="capsl API",
    default_version="v1",
    description="API documentation for capsl App",
)

schema_view = get_schema_view(
    api_info,
    public=True,
)

urlpatterns += [
    path("api-docs/", schema_view.with_ui("swagger", cache_timeout=0), name="api_docs")
]
