# -*- coding: utf-8 -*-
import unittest
from unittest.mock import patch


from dashboard import controller
from dashboard.config import config
from dashboard.db import db
from dashboard.exceptions import PageOutOfRange


@patch('dashboard.controller.render_template')
@patch('dashboard.db.connect')
class TestControllerBuildsetHistory(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        db.bind(provider=config['database']['provider'],
                filename=config['database']['filename'])
        db.generate_mapping(create_tables=True)

    @classmethod
    def tearDownClass(cls):
        db.disconnect()

    def test_can_invoke_show_build(self, *args):
        controller.show_builds_history(page=1)

    def test_page_out_of_range_should_raise_exception(self, *args):
        with self.assertRaises(PageOutOfRange):
            controller.show_builds_history(page=2)

    def test_page_very_out_of_range_should_raise_exception(self, *args):
        with self.assertRaises(PageOutOfRange):
            controller.show_builds_history(page=2346122865)

    def test_page_negative_should_raise_exception(self, *args):
        with self.assertRaises(PageOutOfRange):
            controller.show_builds_history(page=-1)

    def test_page_zero_should_raise_exception(self, *args):
        with self.assertRaises(PageOutOfRange):
            controller.show_builds_history(page=0)
