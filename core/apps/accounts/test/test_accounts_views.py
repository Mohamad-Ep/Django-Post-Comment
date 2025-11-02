import pytest
from django.test import Client
from apps.accounts.models import CustomUser
from django.urls import reverse

# _______________________________________________________


@pytest.fixture
def client():
    client = Client()
    return client


# ----------------------------------
@pytest.fixture
def user_client():
    user = CustomUser.objects.create_user(
        email="test@gmail.com",
        password="Aa123456789@",
        is_active=True,
        is_verified=True,
    )
    return user


# ----------------------------------


@pytest.mark.django_db
class TestAccountView:
    def test_get_register_user_response_ok(self, client):
        url = reverse("accounts:register")
        response = client.get(url)
        assert response.status_code == 200

    def test_post_register_user_response_200(self, client):
        url = reverse("accounts:register")
        data = {"email": "testuser@gmail.com", "password": "asdA1254#"}
        response = client.post(url, data)
        assert response.status_code == 200


# _______________________________________________________
