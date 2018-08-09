# -*- coding: utf-8 -*-
import unittest

from acid import db


class IntegrationTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        db.connect()

    @classmethod
    def tearDownClass(cls):
        db.db.disconnect()
