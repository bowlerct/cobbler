import pytest

from django.urls import reverse


# test authentication required

@pytest.mark.parametrize("view", ["index", "setting_list", "aifile_list", "snippet_list",
                                    "events", "import_prompt", "check"])
def test_redirect_to_login_on_get(client, view):
    response = client.get( reverse(view) )

    assert response.status_code == 200
    # not authenticated - ensure we are redirected to login page 
    assert 'login.tmpl' in (t.name for t in response.templates)

# FIXME
# what_list -> requires args=[what,1]
# Add checks for POST methods as well

# def test_redirect_to_login_on_post(client, view):
#    pass

# test login

def test_index(login_web):
    # we don't use 'next' in order to fully test views.do_login
    client, response = login_web()
    assert response["location"] == '/cobbler_web'

    response = client.get( reverse('index') )

    assert response.status_code == 200
    assert 'index.tmpl' in (t.name for t in response.templates)
    assert b'Welcome to <a href="https://cobbler.github.io/">Cobbler' in response.content
    assert 'cobbler' == response.context['username']


def test_login_with_redirect(login_web):
    client, response = login_web( reverse('events') )

    assert response.status_code == 200
    assert b'Events' in response.content
