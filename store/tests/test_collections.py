from rest_framework import status
from rest_framework.test import APIClient
import pytest

@pytest.mark.django_db
class TestCreateCollection:
    def test_if_user_is_anonymous_returns_401(self):
    #     # arrange
    #     # act
        client = APIClient()
        response = client.post('/store/collections/', data={'title': 'a'})
        # assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.skip
    def test_skip(self):
        assert False