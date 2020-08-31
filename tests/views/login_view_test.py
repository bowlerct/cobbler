import pytest

# from django.conf.urls import url
from django.urls import reverse
#from cobbler.web import urls


def test_redirect_to_login(client):
    response = client.get( reverse('index') )

    assert response.status_code == 200
    assert 'login.tmpl' in (t.name for t in response.templates)


def test_index(client, login_web):
    login_web()
    response = client.get( reverse('index') )
    
    assert 'index.tmpl' in (t.name for t in response.templates)
    assert b'Welcome to <a href="https://cobbler.github.io/">Cobbler' in response.content
    assert 'cobbler' == response.context['username']