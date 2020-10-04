from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from rest_framework import permissions, status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema

from .serializers import (
    SignupSerializer,
    UserSerializer,
    UserGravatarSerializer
)
from users.permissions import (
    SuperUserOrStaffOnly
)

User = get_user_model()


class SignupViewSet(ModelViewSet):
    serializer_class = SignupSerializer
    http_method_names = ["post"]

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)

        return Response({
            'user': serializer.data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })


class UserViewSet(ModelViewSet):
    serializer_class = SignupSerializer
    permission_classes=(
        permissions.IsAuthenticated,
        SuperUserOrStaffOnly
    )
    http_method_names = ["get"]
    
    def get_queryset(self):
        return User.objects.all()

    @swagger_auto_schema(methods=['get'], 
        responses={status.HTTP_200_OK: UserGravatarSerializer})
    @action(methods=['get'], detail=True, url_path='gravatar', url_name='gravatar')
    def gravatar(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)

        return Response(UserGravatarSerializer(user).data)
