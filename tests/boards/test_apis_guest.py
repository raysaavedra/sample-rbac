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


@pytest.mark.django_db
def test_board_list_success_for_guest(client):
    url = reverse('boards-list')

    res = client.get(url)

    assert res.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_board_detail_success_for_guest(client):
    board = baker.make(Board)

    url = reverse('boards-detail', args=[board.id])

    res = client.get(url)

    assert res.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_board_create_success_for_guest(client):
    url = reverse('boards-list')

    topic = baker.make(Topic)

    res = client.post(url, 
        json.dumps(
            {
                'title': 'test', 
                'topic': topic.id,
            }
        ),
        content_type='application/json',)

    assert res.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.django_db
def test_board_update_success_for_guest(client):
    topic = baker.make(Topic)
    board = baker.make(Board, topic=topic)

    url = reverse('boards-detail', args=[board.id])

    res = client.put(url, 
        json.dumps(
            {
                'title': 'test', 
                'topic': topic.id,
            }
        ),
        content_type='application/json',)

    assert res.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.django_db
def test_board_delete_success_for_guest(client):
    topic = baker.make(Topic)
    board = baker.make(Board, topic=topic)

    url = reverse('boards-detail', args=[board.id])

    res = client.delete(url)

    assert res.status_code == status.HTTP_401_UNAUTHORIZED
