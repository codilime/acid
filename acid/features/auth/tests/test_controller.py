# -*- coding: utf-8 -*-
import pytest

from acid.app import app

from .. import service


@pytest.mark.integration
@pytest.mark.auth
class TestSignInAndOut:
    def run_scenario(self):
        client = app.test_client()

        # step 1 log in
        r_in = client.get('/signed_in', follow_redirects=True)
        assert bytes(self.user.full_name, 'utf8') in r_in.data
        assert b'Sign out' in r_in.data

        # step 2 log out
        r_out = client.get('/sign_out', follow_redirects=True)
        assert bytes(self.user.full_name, 'utf8') not in r_out.data
        assert b'Sign in' in r_out.data

    @pytest.mark.parametrize("role", ["admin", "guest"])
    def test_for_user(self, role, get_user, mocker):
        self.user = get_user(role)

        fetch_data = mocker.patch.object(service, 'fetch_user_data')
        fetch_data.return_value = self.user
        with app.test_request_context():
            self.run_scenario()


@pytest.mark.integration
@pytest.mark.auth
def test_redirect_to_launchpad_to_sign_in():
    with app.test_request_context():
        client = app.test_client()
        rv = client.get('/sign_in')
        assert rv.location.startswith('https://login.launchpad.net/+openid')
