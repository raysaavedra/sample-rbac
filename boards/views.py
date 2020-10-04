from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model

from rolepermissions.checkers import has_role
from rolepermissions.roles import assign_role

from boards.models import (
    Board,
)

User = get_user_model()


# this is really an ugly solution
# but just wanted to have a simple view to handle accept
# will update this to a better way if I have more time

def accept(request, board_id, user_id):
    user = get_object_or_404(User, pk=user_id)

    if has_role(user, 'board_moderator'):
        return render(request, 'boards/success.html', {})

    context = {
        'b_id': board_id,
        'u_id': user_id,
    }
    return render(request, 'boards/accept.html', context)


def success(request, board_id, user_id):
    user = get_object_or_404(User, pk=user_id)
    board = get_object_or_404(Board, pk=board_id)

    assign_role(user, 'board_moderator')

    board.moderators.add(user)

    return render(request, 'boards/success.html', {})
