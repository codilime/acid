# -*- coding: utf-8 -*-
import requests

import re
from unittest.mock import patch

from acid.app import app
from acid.tests import IntegrationTestCase


@patch('acid.features.history.controller.db.connect')
class TestControllerBuildHistory(IntegrationTestCase):
    def test_can_invoke_show_history_filterd_by_branch(self, *args):
        with app.test_client() as client:
            rv = client.get('/builds/1?branch=master')
            # Here we use regular expression to evade possible
            # changes in styling of the input form.
            reg_exp = b'<option[^>]+ selected="selected"[^>]>master</option>'
            result = re.search(reg_exp, rv.data)
            self.assertIsNotNone(result)

    def test_can_invoke_show_history_filterd_by_build(self, *args):
        with app.test_client() as client:
            rv = client.get('/builds/1?build=121')
            # Here we use regular expression to evade possible
            # changes in styling of the input form.
            reg_exp = b'<input type="text" name="build"[^>]+value="121'
            result = re.search(reg_exp, rv.data)
            self.assertIsNotNone(result)

    def test_page_out_of_range_should_display_site_not_found(self, *args):
        with app.test_client() as client:
            rv = client.get('/builds/123')
            self.assertIn(b'Site was not found', rv.data)
            self.assertEqual(rv._status_code, requests.codes.not_found)

    def test_page_very_out_of_range_should_display_site_not_found(self, *args):
        with app.test_client() as client:
            rv = client.get('/builds/2346122865')
            self.assertIn(b'Site was not found', rv.data)
            self.assertEqual(rv._status_code, requests.codes.not_found)

    def test_page_negative_should_display_site_not_found(self, *args):
        with app.test_client() as client:
            rv = client.get('/builds/-1')
            self.assertIn(b'Site was not found', rv.data)
            self.assertEqual(rv._status_code, requests.codes.not_found)

    def test_page_zero_should_display_site_not_found(self, *args):
        with app.test_client() as client:
            rv = client.get('/builds/0')
            self.assertIn(b'Site was not found', rv.data)
            self.assertEqual(rv._status_code, requests.codes.not_found)
