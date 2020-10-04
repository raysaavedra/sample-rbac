from django.urls import path, include
from rest_framework.routers import DefaultRouter

from users.api.v1.viewsets import (
    SignupViewSet,
    UserViewSet,
)

router = DefaultRouter()
router.register("signup", SignupViewSet, basename="signup")
router.register("user", UserViewSet, basename="user")

urlpatterns = [
    path("", include(router.urls)),
]
