from django.shortcuts import get_object_or_404

from rest_framework.permissions import BasePermission
from rolepermissions.checkers import has_permission

from boards.models import Board, Thread
from sample_rbac.roles import (
    BoardAdmin,
    BoardModerator,
    ThreadAdmin,
)


class BaseBoardPermission(BasePermission):
    message = 'Permission not allowed. Please register/login to continue.'

    def _role_check(self, user, model, method):
        if method == 'DELETE':
            perm = f'delete_{model}'
        elif method == 'PUT':
            perm = f'change_{model}'
        else:
            perm = f'add_{model}'

        return has_permission(user, perm)

    def _is_moderator(self, request, obj):
        if request.method == 'PUT':
            if obj.__class__.__name__.lower() == 'thread':
                board = obj.board
            else:
                board = obj.thread.board

            if board.moderators.filter(pk=request.user.pk).exists():
                return True
        
        return False


class BoardObjPermissions(BaseBoardPermission):
    
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff or request.user.is_superuser:
            return True

        if not self._role_check(request.user, 
            obj.__class__.__name__.lower(), 
            request.method
        ):
            return False

        if obj.admin == request.user:
            return True
        
        return False


class ThreadObjPermissions(BaseBoardPermission):

    def has_object_permission(self, request, view, obj):
        if (request.user.is_staff or request.user.is_superuser):
            return True

        if not self._role_check(request.user, 
            obj.__class__.__name__.lower(), 
            request.method
        ):
            return False
        
        if (obj.board.admin == request.user) or \
            (obj.admin == request.user) or \
            self._is_moderator(request, obj):
            return True

        return False


class PostObjPermissions(BaseBoardPermission):

    def has_object_permission(self, request, view, obj):
        if (request.user.is_staff or request.user.is_superuser):
            return True

        if not self._role_check(request.user, 
            obj.__class__.__name__.lower(), 
            request.method
        ):
            return False
        
        if (obj.thread.board.admin == request.user) or \
            (obj.thread.admin == request.user) or \
            (obj.user == request.user) or \
            self._is_moderator(request, obj):
            return True

        return False
