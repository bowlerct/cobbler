import pytest

# from django.conf.urls import url
from django.urls import reverse


def test_redirect_to_login(client):
    response = client.get( reverse('index'), follow=False )

    assert response.status_code == 302
    assert response["Location"] == reverse ('login')
