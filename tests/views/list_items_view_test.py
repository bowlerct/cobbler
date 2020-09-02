import pytest

from django.urls import reverse
from cobbler import api as cobbler_api


# Settings

def test_settings_list(login_web):
    client, response = login_web( reverse('setting_list') )

    assert response.status_code == 200
    assert 'settings.tmpl' in (t.name for t in response.templates)

    # ensure all settings are listed
    api = cobbler_api.CobblerAPI()
    settings = api.settings().to_dict()
    for k in settings.keys():
        assert k.encode('utf-8') in response.content


# autoinstall files

def test_aifile_list(login_web):
    client, response = login_web( reverse('aifile_list') )

    assert response.status_code == 200
    assert 'aifile_list.tmpl' in (t.name for t in response.templates)
    assert b'sample.ks' in response.content


# snippet files

def test_snippet_list(login_web):
    client, response = login_web( reverse('snippet_list') )

    assert response.status_code == 200
    assert 'snippet_list.tmpl' in (t.name for t in response.templates)
    assert b'cobbler_register' in response.content


# generic lists

@pytest.mark.parametrize("what", ["distro", "profile", "system", "image",
                                    "repo", "package", "mgmtclass", "file"])
def test_generic_list(login_web, what):
    client, response = login_web( reverse('what_list', args=[what, 1]) )
    #response = client.get( reverse('what_list', args=[what, 1]) )

    assert response.status_code == 200
    assert 'generic_list.tmpl' in (t.name for t in response.templates)
    assert b'Name' in response.content


# FIXME test actions 'check' and 'sync' first so there are logs for events check to succeed


def test_events_list(login_web):
    client, response = login_web( reverse('events') )

    assert b'Events' in response.content

    # requires at least one event has occurred
    # assert b'/cobbler_web/eventlog/' in response.content
