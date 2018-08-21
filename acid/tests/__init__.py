# -*- coding: utf-8 -*-
from acid import db


class IntegrationTestCase:
    @classmethod
    def setup_class(cls):
        db.connect()

    @classmethod
    def teardown_class(cls):
        db.db.disconnect()
