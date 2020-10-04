import json

from django.contrib.auth import get_user_model

import pytest
from rest_framework import status
from rest_framework.reverse import reverse
from model_bakery import baker

User = get_user_model()

def _setup_user():
    user = baker.make(User, username='test1')
    user.set_password('test123!@#')
    user.save()

    return user

@pytest.mark.django_db
def test_sign_up(api_client):
    url = reverse('signup-list')

    res = api_client.post(url,
        json.dumps(
            {
                'email': 'test1@test.com', 
                'password': 'test123!@#', 
                'username': 'test1'
            }
        ),
        content_type='application/json',
    )

    assert res.status_code == status.HTTP_200_OK
    assert res.json()['user']['email'] == 'test1@test.com'

@pytest.mark.django_db
def test_sign_up_returns_jwt_tokens(api_client):
    url = reverse('signup-list')

    res = api_client.post(url,
        json.dumps(
            {
                'email': 'test1@test.com', 
                'password': 'test123!@#', 
                'username': 'test1'
            }
        ),
        content_type='application/json',
    )

    assert res.status_code == status.HTTP_200_OK
    assert res.json()['access']
    assert res.json()['refresh']

@pytest.mark.django_db
def test_login(client):
    _setup_user()

    url = reverse('login')
    res = client.post(url,
        json.dumps(
            {
                'password': 'test123!@#', 
                'username': 'test1'
            }
        ),
        content_type='application/json',
    )

    assert res.status_code == status.HTTP_200_OK
    assert res.json()['access']
    assert res.json()['refresh']

@pytest.mark.django_db
def test_login_fail(client):
    _setup_user()

    url = reverse('login')
    res = client.post(url,
        json.dumps(
            {
                'password': 'test123!@#123', 
                'username': 'test1'
            }
        ),
        content_type='application/json',
    )

    assert res.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.django_db
def test_get_gravatar_no_auth(client):
    user = _setup_user()

    url = reverse('user-gravatar', args=[user.id])
    res = client.get(url)

    assert res.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.django_db
def test_get_gravatar_null(api_client):
    user = api_client.user
    user.is_superuser = True
    user.save()

    url = reverse('user-gravatar', args=[user.id])
    res = api_client.get(url)

    assert res.status_code == status.HTTP_200_OK
    assert res.json()['gravatar'] == None

@pytest.mark.django_db
def test_get_gravatar_success(gravatar_client):
    user = gravatar_client.user
    user.is_superuser = True
    user.save()

    url = reverse('user-gravatar', args=[user.id])
    res = gravatar_client.get(url)

    assert res.status_code == status.HTTP_200_OK
    assert res.json()['gravatar'] != None
