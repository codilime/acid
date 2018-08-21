# -*- coding: utf-8 -*-
import os
import pytest

from ...auth.tests.conftest import get_user, user_admin, user_guest  # noqa F401


@pytest.fixture
def path_to_test_file():
    rootdir = os.path.dirname(os.path.abspath(__file__))

    def _path_to_test_file(filename):
        return os.path.join(rootdir, 'static', filename)

    return _path_to_test_file
