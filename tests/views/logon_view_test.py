import pytest

from django.urls import reverse


# test authentication required for all views and urls
# test login view and redirection

# HTTP GET methods

# FIXME add edit urls as they use GET
@pytest.mark.parametrize("what", [("index",[]), ("setting_list",[]), ("aifile_list",[]),
                            ("snippet_list",[]), ("events",[]), ("import_prompt",[]),
                            ("check",[]), ("what_list", ["distro"]), ("what_list", ["profile"]),
                            ("what_list", ["system"]), ("what_list", ["image"]), 
                            ("what_list", ["repo"]), ("what_list", ["package"]),
                            ("what_list", ["mgmtclass"]), ("what_list", ["file"]),
                            ("snippet_list", []), ("aifile_list", []), ("setting_list", []),
                            ("events",[]), ("events_log",["time"]), ("check", []),
                            ("task_created", []), ("import_prompt", []),
                            ("utils_random_mac", []), ("utils_random_mac_virttype", ["xenpv"])])
def test_redirect_to_login_on_get(client, what):
    view, args = what
    response = client.get( reverse(view, args=args) )

    assert response.status_code == 200
    # not authenticated - ensure we are redirected to login page 
    assert 'login.tmpl' in (t.name for t in response.templates)


# HTTPD POST methods

@pytest.mark.parametrize("what", [("setting_save", []),
                                ("aifile_save", []),
                                ("snippet_save", []),
                                ("what_save", ['distro']),
                                ("what_modifylist", ['distro', 'limit', '10']),
                                ("what_remame", ['distro','RH8','RH8-x86_84']),
                                ("what_copy", ['distro','RH8','RH8-copy']),
                                ("what_delete", ['distro', 'RH8']),
                                ("what_domulti", ['system', 'profile', 'profile']),
                                ("buildiso", []),
                                ("import_run", []),
                                ("sync", []),
                                ("reposync", []),
                                ("hardlink", []),
                                ("replicate", [])])
def test_redirect_to_login_on_post(client, what):
    view, args = what

    # we do not need to post data as the first operation the
    # views should do is to verify client is authenticated
    response = client.post( reverse(view, args=args) )

    assert response.status_code == 200
    # not authenticated - ensure we are redirected to login page 
    assert 'login.tmpl' in (t.name for t in response.templates)


# test login operation

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
