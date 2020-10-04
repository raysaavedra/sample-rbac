import json

from django.contrib.auth import get_user_model

import pytest
from rest_framework import status
from rest_framework.reverse import reverse
from model_bakery import baker
from rolepermissions.roles import assign_role

from boards.models import (
    Board,
    Topic,
    Thread,
    Post
)

User = get_user_model()

def _setup_user(user):
    user.is_superuser = False
    user.is_staff = False
    assign_role(user, 'board_moderator')
    user.save()

@pytest.mark.django_db
def test_posts_list_success_for_board_moderator(api_client):
    _setup_user(api_client.user)
    url = reverse('posts-list')

    res = api_client.get(url)

    assert res.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_posts_detail_success_for_board_moderator(api_client):
    _setup_user(api_client.user)
    topic = baker.make(Topic)
    board = baker.make(Board, topic=topic)
    thread = baker.make(Thread, board=board)
    post = baker.make(Post, thread=thread)

    url = reverse('posts-detail', args=[post.id])

    res = api_client.get(url)

    assert res.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_posts_create_success_for_board_moderator(api_client):
    _setup_user(api_client.user)
    url = reverse('posts-list')

    topic = baker.make(Topic)
    board = baker.make(Board, topic=topic)
    board.moderators.add(api_client.user)
    thread = baker.make(Thread, board=board)

    res = api_client.post(url, 
        json.dumps(
            {
                'message': 'test', 
                'thread': thread.id,
            }
        ),
        content_type='application/json',)

    assert res.status_code == status.HTTP_201_CREATED

@pytest.mark.django_db
def test_posts_update_success_for_board_moderator(api_client):
    _setup_user(api_client.user)
    topic = baker.make(Topic)
    board = baker.make(Board, topic=topic)
    board.moderators.add(api_client.user)
    thread = baker.make(Thread, board=board)
    post = baker.make(Post, thread=thread)

    url = reverse('posts-detail', args=[post.id])

    res = api_client.put(url, 
        json.dumps(
            {
                'message': 'test', 
                'thread': thread.id,
            }
        ),
        content_type='application/json',)

    assert res.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_posts_delete_fail_for_board_moderator(api_client):
    _setup_user(api_client.user)
    topic = baker.make(Topic)
    board = baker.make(Board, topic=topic)
    board.moderators.add(api_client.user)
    thread = baker.make(Thread, board=board)
    post = baker.make(Post, thread=thread)

    url = reverse('posts-detail', args=[post.id])

    res = api_client.delete(url)

    assert res.status_code == status.HTTP_403_FORBIDDEN
