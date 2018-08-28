# -*- coding: utf-8 -*-
import pytest

from flask import current_app

from acid.tests import TestWithAppContext

from ..model import User, get_current_user


@pytest.mark.unit
class TestUserModel(TestWithAppContext):
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
        mocker.patch.dict(current_app.config['default'], {
                          'users_file': 'nofile'})
        with pytest.raises(FileNotFoundError):
            user_guest.is_admin()

    def test_get_current_user_return_none_when_session_not_exist(self, mocker):
        mocker.patch('acid.features.auth.model.session', None)
        assert get_current_user() is None

    def test_get_current_user_return_proper_user_when_session(self, mocker):
        mocker.patch('acid.features.auth.model.session', {'user': 'test_user'})
        assert get_current_user() == 'test_user'
