import pytest
from django.urls import reverse

@pytest.fixture(scope="function")
def login_web(client):
    def _login_web():
        data = {'username': 'cobbler', 'password': 'cobbler'}
        client.post(reverse('do_login'), data)

    return _login_web