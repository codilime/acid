# -*- coding: utf-8 -*-
import pytest

from ..model import User


@pytest.fixture
def user_admin():
    """Return User object with admin privileges."""
    return User(full_name='Admin Admin', email='admin@acid.test')


@pytest.fixture
def user_guest():
    """Return User object with guest privileges."""
    return User(full_name='Noname Guest', email='noname@guest.test')


@pytest.fixture
def get_user(user_admin, user_guest):
    return lambda x: user_admin if x == 'admin' else user_guest
