# -*- coding: utf-8 -*-
import unittest
from unittest.mock import patch

import pytest

from acid.config import config

from . import fixtures


@pytest.mark.unit
class TestUsers(unittest.TestCase):
    def test_user_is_admin_should_return_true(self):
        user = fixtures.UserFactory.get_user(fixtures.UserFactory.ROLE_ADMIN)
        self.assertTrue(user.is_admin())

    def test_user_not_admin_should_return_false(self):
        user = fixtures.UserFactory.get_user(fixtures.UserFactory.ROLE_USER)
        self.assertFalse(user.is_admin())

    def test_no_users_file_should_raise_exception(self):
        user = fixtures.UserFactory.get_user(fixtures.UserFactory.ROLE_USER)
        with patch.dict(config['default'], {'users_file': 'nofile'}):
            with self.assertRaises(FileNotFoundError):
                user.is_admin()

    def test_none_as_email_should_return_false(self):
        user = fixtures.UserFactory.get_user(fixtures.UserFactory.ROLE_ADMIN)
        user.email = None
        self.assertFalse(user.is_admin())
