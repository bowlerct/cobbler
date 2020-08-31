import pytest

from django.urls import reverse
from cobbler import api as cobbler_api


def test_redirect_to_login(client):
    response = client.get( reverse('index') )

    assert response.status_code == 200
    assert 'login.tmpl' in (t.name for t in response.templates)


def test_index(login_web):
    client = login_web()
    response = client.get( reverse('index') )

    assert response.status_code == 200
    assert 'login.tmpl' in (t.name for t in response.templates)
    assert 'index.tmpl' in (t.name for t in response.templates)
    assert b'Welcome to <a href="https://cobbler.github.io/">Cobbler' in response.content
    assert 'cobbler' == response.context['username']


def test_settings_list(client, login_web):
    login_web()
    response = client.get( reverse('setting_list') )

    assert 'settings.tmpl' in (t.name for t in response.templates)

    # ensure all settings are listed
    api = cobbler_api.CobblerAPI()
    settings = api.settings().to_dict()
    for k in settings.keys():
        assert k.encode('utf-8') in response.content
