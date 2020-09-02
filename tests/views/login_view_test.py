import pytest

from django.urls import reverse
from cobbler import api as cobbler_api


def test_redirect_to_login(client):
    response = client.get( reverse('index') )

    assert response.status_code == 200
    # ensure we were redirected to login page
    assert 'login.tmpl' in (t.name for t in response.templates)


def test_index(login_web):
    client = login_web()
    response = client.get( reverse('index') )

    assert 'index.tmpl' in (t.name for t in response.templates)
    assert b'Welcome to <a href="https://cobbler.github.io/">Cobbler' in response.content
    assert 'cobbler' == response.context['username']


# Settings

def test_settings_list(login_web):
    client = login_web()
    response = client.get( reverse('setting_list') )

    assert 'settings.tmpl' in (t.name for t in response.templates)

    # ensure all settings are listed
    api = cobbler_api.CobblerAPI()
    settings = api.settings().to_dict()
    for k in settings.keys():
        assert k.encode('utf-8') in response.content

# autoinstall files

def test_aifile_list(login_web):
    client = login_web()
    response = client.get( reverse('aifile_list') )

    assert 'aifile_list.tmpl' in (t.name for t in response.templates)
    assert b'sample.ks' in response.content

# snippet files

def test_snippet_list(login_web):
    client = login_web()
    response = client.get( reverse('snippet_list') )

    assert 'snippet_list.tmpl' in (t.name for t in response.templates)
    assert 'cobbler_register' in response.content

# generic lists

@pytest.mark.parametrize("what", ["distro", "profile", "system", "image",
                                    "repo", "package", "mgmtclass", "file"])
def test_generic_list(login_web, what):
    client = login_web()
    response = client.get( reverse('what_list', kwargs={'what': what, 'page': 1}) )

    assert response.status_code == 200
    assert 'generic_list.tmpl' in (t.name for t in response.templates)
    assert b'Name' in response.content

def test_events_list(login_web):
    client = login_web()
    response = client.get( reverse('events') )
