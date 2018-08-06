# -*- coding: utf-8 -*-
import unittest

from pony.orm import db_session

from dashboard import db

from tests import fixtures


class IntegrationTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        db.connect()

    @classmethod
    def tearDownClass(cls):
        db.db.disconnect()

    @classmethod
    @db_session
    def seed_database(cls):
        fixtures.seed_database()
