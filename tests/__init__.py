# -*- coding: utf-8 -*-
import unittest

from pony.orm import db_session

from dashboard import db

from dashboard.auth.tests import fixtures


class IntegrationTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        db.connect()

    @classmethod
    def tearDownClass(cls):
        db.db.disconnect()
