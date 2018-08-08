# -*- coding: utf-8 -*-
import unittest
from unittest import mock

from app import app

from dashboard.auth.tests.fixtures import UserFactory


@mock.patch('dashboard.auth.service.fetch_user_data')
class TestAuthControllers(unittest.TestCase):
    def test_user_can_sign_in_and_sign_out(self, fetch_data):
        cases = (UserFactory.ROLE_ADMIN, UserFactory.ROLE_USER)

        with app.test_request_context():
            with app.test_client() as client:
                for case in cases:
                    user = UserFactory.get_user(role=case)
                    fetch_data.return_value = user

                    # step 1 log in
                    r_in = client.get('/signed_in', follow_redirects=True)
                    self.assertIn(bytes(user.full_name, 'utf8'), r_in.data)
                    self.assertIn(b'Sign out', r_in.data)

                    # step 2 log out
                    r_out = client.get('/sign_out', follow_redirects=True)
                    self.assertNotIn(bytes(user.full_name, 'utf8'), r_out.data)
                    self.assertIn(b'Sign in', r_out.data)

    def test_can_be_succesfull_redirect_to_openid_provider(self, *args):
        with app.test_request_context():
            with app.test_client() as client:
                r_in = client.get('/sign_in')
                self.assertIn('https://login.launchpad.net/+openid',
                              r_in.location)
