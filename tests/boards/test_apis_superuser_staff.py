import json

from django.contrib.auth import get_user_model

import pytest
from rest_framework import status
from rest_framework.reverse import reverse
from model_bakery import baker

from boards.models import (
    Board,
    Topic
)

User = get_user_model()

def _setup_user(user):
    user.is_superuser = True
    user.is_staff = True
    user.save()

@pytest.mark.django_db
def test_board_list_success_for_superuser_or_staff(api_client):
    _setup_user(api_client.user)
    url = reverse('boards-list')

    res = api_client.get(url)

    assert res.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_board_detail_success_for_superuser_or_staff(api_client):
    _setup_user(api_client.user)
    board = baker.make(Board)

    url = reverse('boards-detail', args=[board.id])

    res = api_client.get(url)

    assert res.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_board_create_fail_for_superuser_or_staff(api_client):
    _setup_user(api_client.user)
    url = reverse('boards-list')

    topic = baker.make(Topic)

    res = api_client.post(url, 
        json.dumps(
            {
                'title': 'test', 
                'topic': topic.id,
            }
        ),
        content_type='application/json',)

    assert res.status_code == status.HTTP_201_CREATED

@pytest.mark.django_db
def test_board_update_fail_for_superuser_or_staff(api_client):
    _setup_user(api_client.user)
    topic = baker.make(Topic)
    board = baker.make(Board, topic=topic)

    url = reverse('boards-detail', args=[board.id])

    res = api_client.put(url, 
        json.dumps(
            {
                'title': 'test', 
                'topic': topic.id,
            }
        ),
        content_type='application/json',)

    assert res.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_board_delete_fail_for_superuser_or_staff(api_client):
    _setup_user(api_client.user)
    topic = baker.make(Topic)
    board = baker.make(Board, topic=topic)

    url = reverse('boards-detail', args=[board.id])

    res = api_client.delete(url)

    assert res.status_code == status.HTTP_204_NO_CONTENT
