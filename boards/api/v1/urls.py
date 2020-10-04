from django.urls import path, include
from rest_framework.routers import DefaultRouter

from boards.api.v1.viewsets import (
    BoardViewSet,
    ThreadViewSet,
    PostViewSet
)

router = DefaultRouter()
router.register("boards", BoardViewSet, basename="boards")
router.register("threads", ThreadViewSet, basename="threads")
router.register("posts", PostViewSet, basename="posts")

urlpatterns = [
    path("", include(router.urls)),
]
