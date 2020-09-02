import pytest
from django.urls import reverse


@pytest.fixture(scope="function")
def login_web(client):
    def _login_web(next=""):
        data = {'username': 'cobbler', 'password': 'cobbler', 'next': next}
        response = client.post(reverse('do_login'), data, follow=True)
        return client, response
    return _login_web
