# -*- coding: utf-8 -*-
import unittest
from unittest.mock import patch

from dashboard.users import is_admin
from dashboard.config import config


class TestUsers(unittest.TestCase):
    def test_user_is_admin_should_return_true(self):
        result = is_admin(email="me@example.com")
        self.assertTrue(result)

    def test_user_not_admin_should_return_false(self):
        result = is_admin(email="not@admin.com")
        self.assertFalse(result)

    def test_no_users_file_should_raise_exception(self):
        with patch.dict(config['default'], {'users_file': 'nofile'}):
            with self.assertRaises(FileNotFoundError):
                is_admin(email="a@b.com")

    def test_none_as_email_sould_return_false(self):
        result = is_admin(email=None)
        self.assertFalse(result)
