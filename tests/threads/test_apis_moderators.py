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
    Thread
)

User = get_user_model()

def _setup_user(user):
    user.is_superuser = False
    user.is_staff = False
    assign_role(user, 'board_moderator')
    user.save()

@pytest.mark.django_db
def test_thread_list_success_for_moderator(api_client):
    _setup_user(api_client.user)
    url = reverse('threads-list')

    res = api_client.get(url)

    assert res.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_thread_detail_success_for_moderator(api_client):
    _setup_user(api_client.user)
    board = baker.make(Board)
    thread = baker.make(Thread, board=board)

    url = reverse('threads-detail', args=[thread.id])

    res = api_client.get(url)

    assert res.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_thread_create_success_for_moderator(api_client):
    _setup_user(api_client.user)
    url = reverse('threads-list')

    board = baker.make(Board)
    board.moderators.add(api_client.user)

    res = api_client.post(url, 
        json.dumps(
            {
                'title': 'test', 
                'board': board.id,
            }
        ),
        content_type='application/json',)

    assert res.status_code == status.HTTP_201_CREATED

@pytest.mark.django_db
def test_thread_update_fail_for_not_moderator_on_thread(api_client):
    _setup_user(api_client.user)

    board = baker.make(Board)
    thread = baker.make(Thread, board=board)

    url = reverse('threads-detail', args=[thread.id])

    res = api_client.put(url, 
        json.dumps(
            {
                'title': 'test', 
                'board': board.id,
            }
        ),
        content_type='application/json',)

    assert res.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.django_db
def test_thread_update_success_for_moderator_on_thread(api_client):
    _setup_user(api_client.user)

    board = baker.make(Board)
    thread = baker.make(Thread, board=board)
    board.moderators.add(api_client.user)

    url = reverse('threads-detail', args=[thread.id])

    res = api_client.put(url, 
        json.dumps(
            {
                'title': 'test1', 
                'board': board.id,
            }
        ),
        content_type='application/json',)

    assert res.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_thread_delete_fail_for_not_moderator_on_thread(api_client):
    _setup_user(api_client.user)

    board = baker.make(Board)
    thread = baker.make(Thread, board=board)

    url = reverse('threads-detail', args=[thread.id])

    res = api_client.delete(url)

    assert res.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.django_db
def test_thread_delete_fail_for_not_admin_on_thread(api_client):
    _setup_user(api_client.user)

    board = baker.make(Board)
    thread = baker.make(Thread, board=board)
    board.moderators.add(api_client.user)

    url = reverse('threads-detail', args=[thread.id])

    res = api_client.delete(url)

    assert res.status_code == status.HTTP_403_FORBIDDEN
