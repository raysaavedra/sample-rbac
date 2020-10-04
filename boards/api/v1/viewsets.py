from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from .serializers import (
    BoardSerializer,
    ThreadSerializer,
    PostSerializer,
    ModeratorInviteSerializer
)
from boards.permissions import (
    BoardObjPermissions,
    ThreadObjPermissions,
    PostObjPermissions
)
from boards.models import (
    Board,
    Thread,
    Post
)

User = get_user_model()


class BoardViewSet(ModelViewSet):
    serializer_class = BoardSerializer
    http_method_names = ["post", "get", "put", "delete"]

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = [permissions.AllowAny]
        elif self.request.method == 'POST':
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [BoardObjPermissions]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        topic = self.request.GET.get('topic')
        order = self.request.GET.get('order')

        filters = {}

        if topic:
            filters['topic'] = topic

        board = Board.objects.filter(**filters)

        if order:
            if order == 'up':
                board = board.order_by('-created_at')
            else:
                board = board.order_by('created_at')

        return board

    @swagger_auto_schema(methods=['post'], 
        request_body=ModeratorInviteSerializer,
        responses={status.HTTP_200_OK: ModeratorInviteSerializer})
    @action(methods=['post'], detail=True, url_path='moderator-invite', url_name='moderator_invite')
    def moderator_invite(self, request, pk=None):
        serializer = ModeratorInviteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = get_object_or_404(User, pk=serializer.validated_data['user_id'])
        board = get_object_or_404(Board, pk=pk)

        # ugly way on creating an invite url; needs to be updated
        # will update if I have more time
        return Response({
            'invite_url': board.generate_invite_url(user, request)
        })


class ThreadViewSet(ModelViewSet):
    serializer_class = ThreadSerializer
    http_method_names = ["post", "get", "put", "delete"]

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = [permissions.AllowAny]
        elif self.request.method == 'POST':
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [ThreadObjPermissions]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        filters = {}
        return Thread.objects.filter(**filters)


class PostViewSet(ModelViewSet):
    serializer_class = PostSerializer
    http_method_names = ["post", "get", "put", "delete"]

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = [permissions.AllowAny]
        elif self.request.method == 'POST':
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [PostObjPermissions]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        filters = {}
        return Post.objects.filter(**filters)

