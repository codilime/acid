# -*- coding: utf-8 -*-
from unittest import mock

import pytest

from requests import codes

from acid.app import app
from acid.config import config
from acid.tests import IntegrationTestCase

from ...auth import service as auth_service
from ...auth.tests.fixtures import UserFactory


@pytest.mark.integration
@mock.patch.object(auth_service, 'fetch_user_data')
class TestControlPanel(IntegrationTestCase):
    def test_guest_user_cant_see_zuul_management(self, fetch_data):
        user = UserFactory.get_user(role=UserFactory.ROLE_USER)
        fetch_data.return_value = user
        with app.test_request_context():
            with app.test_client() as client:
                res = client.get('/zuul_manager', follow_redirects=True)

        self.assertEqual(res.status_code, codes.unauthorized)
        self.assertNotIn(b'Zuul manager', res.data)

    def test_admin_user_can_see_zuul_management(self, fetch_data):
        user = UserFactory.get_user(role=UserFactory.ROLE_ADMIN)
        fetch_data.return_value = user
        with app.test_request_context():
            with app.test_client() as client:
                client.get('/signed_in', follow_redirects=True)
                res = client.get('/zuul_manager', follow_redirects=True)

        self.assertEqual(res.status_code, codes.ok)
        # Remove newline characters for easier regex parsing
        rendered_template = res.data.replace(b'\n', b'')
        # Create a pattern that looks for all pairs (pipeline, branch) defined
        # in config. Regex looks inside of body tag in order to ensure it's
        # displayed in specific site content and not in other elements.
        pattern = '<body>.*'
        for pipelines in config['zuul']['build_enqueue']['pipelines']:
            for pipeline, branches in pipelines.items():
                for branch in branches:
                    pattern += '.*'.join([pipeline, branch, 'START', 'STOP.*'])
        pattern += '</body>'
        pattern = str.encode(pattern)
        self.assertRegex(rendered_template, pattern)

    def test_pipeline_not_present_in_config_is_not_displayed(self, fetch_data):
        user = UserFactory.get_user(role=UserFactory.ROLE_ADMIN)
        fetch_data.return_value = user
        with app.test_request_context():
            with app.test_client() as client:
                client.get('/signed_in', follow_redirects=True)
                res = client.get('/zuul_manager', follow_redirects=True)

        self.assertEqual(res.status_code, codes.ok)
        # Remove newline characters for easier regex parsing
        rendered_template = res.data.replace(b'\n', b'')
        # Regex checks if specified pipeline doesn't exist inside of body tag
        pattern = b'(?!<body>.*pipeline_name_not_in_config.*</body>)'
        self.assertRegex(rendered_template, pattern)

    def test_branch_not_present_in_config_is_not_displayed(self, fetch_data):
        user = UserFactory.get_user(role=UserFactory.ROLE_ADMIN)
        fetch_data.return_value = user
        with app.test_request_context():
            with app.test_client() as client:
                client.get('/signed_in', follow_redirects=True)
                res = client.get('/zuul_manager', follow_redirects=True)

        self.assertEqual(res.status_code, codes.ok)
        # Remove newline characters for easier regex parsing
        rendered_template = res.data.replace(b'\n', b'')
        # Regex checks if specified branch doesn't exist inside of body tag
        pattern = b'(?!<body>.*branch_name_not_in_config.*</body>)'
        self.assertRegex(rendered_template, pattern)

    def test_admin_cannot_start_build_not_in_config(self, fetch_data):
        user = UserFactory.get_user(role=UserFactory.ROLE_ADMIN)
        fetch_data.return_value = user
        with app.test_request_context():
            with app.test_client() as client:
                client.get('/signed_in', follow_redirects=True)
                res = client.post('/zuul_manager/manage',
                                  follow_redirects=True,
                                  data={'pipeline_name': 'fake-pipeline',
                                        'branch': 'fake-branch',
                                        'action': 'start'})
        self.assertEqual(res.status_code, codes.bad_request)

    def test_starts_build_successful_connect_to_zuul(self, fetch_data):
        user = UserFactory.get_user(role=UserFactory.ROLE_ADMIN)
        fetch_data.return_value = user
        with app.test_request_context():
            with app.test_client() as client:
                client.get('/signed_in', follow_redirects=True)
                res = client.post('/zuul_manager/manage',
                                  follow_redirects=True,
                                  data={'pipeline_name': 'periodic-nightly',
                                        'branch': 'master',
                                        'action': 'start'})
        self.assertEqual(res.status_code, codes.ok)

    def test_with_incorect_settings_cant_connect_to_zuul(self, fetch_data):
        user = UserFactory.get_user(role=UserFactory.ROLE_ADMIN)
        fetch_data.return_value = user
        with app.test_request_context():
            with app.test_client() as client:
                with mock.patch.dict(config['zuul']['manager'],
                                     {'username': 'not'}):
                    client.get('/signed_in', follow_redirects=True)
                    res = client.post('/zuul_manager/manage',
                                      follow_redirects=True,
                                      data={'pipeline_name': 'periodic-nightly',
                                            'branch': 'master',
                                            'action': 'start'})
        self.assertEqual(res.status_code, codes.server_error)
