# -*- coding: utf-8 -*-
import unittest
from unittest.mock import patch

from dashboard.db import db
from dashboard.exceptions import PageOutOfRange
from dashboard import controller


@patch('dashboard.controller.render_template')
class TestController(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        db.bind(provider='sqlite', filename=':memory:')
        db.generate_mapping(create_tables=True)

    @classmethod
    def tearDownClass(cls):
        db.disconnect()

    def test_can_invoke_show_build(self, render_template):
        controller.show_builds_history(page=1)

    def test_page_out_of_range_should_raise_exception(self, render_template):
        with self.assertRaises(PageOutOfRange):
            controller.show_builds_history(page=2)

    def test_page_very_out_of_range_should_raise_exception(self, renderer):
        with self.assertRaises(PageOutOfRange):
            controller.show_builds_history(page=2346122865)

    def test_page_negative_should_raise_exception(self, render_template):
        with self.assertRaises(PageOutOfRange):
            controller.show_builds_history(page=-1)

    def test_page_zero_should_raise_exception(self, render_template):
        with self.assertRaises(PageOutOfRange):
            controller.show_builds_history(page=0)
