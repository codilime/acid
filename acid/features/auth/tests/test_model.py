# -*- coding: utf-8 -*-
import pytest

from acid.config import config

from ..model import User


@pytest.mark.unit
class TestUserModel:
    def test_create_user_obj(self):
        User(full_name="Test User", email="test.user@acid.test")

    def test_is_admin_should_return_true_for_admin(self, user_admin):
        assert user_admin.is_admin() is True

    def test_is_admin_should_return_false_for_guest(self, user_guest):
        assert user_guest.is_admin() is False

    def test_is_admin_should_return_false_if_user_has_no_email(self):
        user = User(full_name="Test User", email=None)
        assert user.is_admin() is False

    def test_raise_exception_if_user_yml_not_exist(self, user_guest, mocker):
        mocker.patch.dict(config['default'], {'users_file': 'nofile'})
        with pytest.raises(FileNotFoundError):
            user_guest.is_admin()
