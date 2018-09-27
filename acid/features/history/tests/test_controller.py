# -*- coding: utf-8 -*-
import re

import pytest

import requests

from pony.orm import db_session

from acid.app import app
from acid.tests import DatabaseTestCase


@db_session
@pytest.mark.integration
@pytest.mark.history
class TestBuildHistory(DatabaseTestCase):
    client = app.test_client()

    def test_show_history_filtered_by_branch(self, populate_database):
        populate_database(branch='master')
        rv = self.client.get('/builds/1?branch=master')
        # Here we use regular expression to evade possible
        # changes in styling of the input form.
        reg_exp = b'<option[^>]+ selected="selected"[^>]>master</option>'
        assert re.search(reg_exp, rv.data) is not None

    def test_show_history_filtered_by_build_number(self, populate_database):
        populate_database(build_number=121)
        rv = self.client.get('/builds/1?build=121')
        # Here we use regular expression to evade possible
        # changes in styling of the input form.
        reg_exp = b'<input type="text" name="build"[^>]+value="121'
        assert re.search(reg_exp, rv.data) is not None

    @pytest.mark.parametrize("page", [123, 2346122865, -1, 0, 3.5, "five"])
    def test_page_out_of_range_should_return_not_found(self, page,
                                                       populate_database):
        populate_database()
        rv = self.client.get(f'/builds/{page}')
        assert b'Site was not found' in rv.data
        assert rv.status_code == requests.codes.not_found
