from django.contrib.auth import get_user_model

import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

@pytest.fixture
def api_client():
    user = User.objects.create_user(
        username='test', 
        email='test@test.com', 
        password='test123!@#',
    )
    client = APIClient()
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    client.user = user
    client.force_login(user)

    return client

@pytest.fixture
def gravatar_client():
    user = User.objects.create_user(
        username='test', 
        email='rayyacosaavedra@gmail.com', 
        password='test123!@#',
    )
    client = APIClient()
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    client.user = user
    client.force_login(user)

    return client
