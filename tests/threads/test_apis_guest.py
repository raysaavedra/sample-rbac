import json

from django.contrib.auth import get_user_model

import pytest
from rest_framework import status
from rest_framework.reverse import reverse
from model_bakery import baker

from boards.models import (
    Board,
    Topic,
    Thread
)

User = get_user_model()


@pytest.mark.django_db
def test_thread_list_success_for_guest(client):
    url = reverse('threads-list')

    res = client.get(url)

    assert res.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_thread_detail_success_for_guest(client):
    topic = baker.make(Topic)
    board = baker.make(Board, topic=topic)
    thread = baker.make(Thread, board=board)

    url = reverse('threads-detail', args=[thread.id])

    res = client.get(url)

    assert res.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_thread_create_success_for_guest(client):
    url = reverse('threads-list')

    topic = baker.make(Topic)
    board = baker.make(Board, topic=topic)

    res = client.post(url, 
        json.dumps(
            {
                'title': 'test', 
                'board': board.id,
            }
        ),
        content_type='application/json',)

    assert res.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.django_db
def test_thread_update_success_for_guest(client):
    topic = baker.make(Topic)
    board = baker.make(Board, topic=topic)
    thread = baker.make(Thread, board=board)

    url = reverse('threads-detail', args=[thread.id])

    res = client.put(url, 
        json.dumps(
            {
                'title': 'test', 
                'board': board.id,
            }
        ),
        content_type='application/json',)

    assert res.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.django_db
def test_thread_delete_success_for_guest(client):
    topic = baker.make(Topic)
    board = baker.make(Board, topic=topic)
    thread = baker.make(Thread, board=board)

    url = reverse('threads-detail', args=[thread.id])

    res = client.delete(url)

    assert res.status_code == status.HTTP_401_UNAUTHORIZED
