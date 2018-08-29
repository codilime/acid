# -*- coding: utf-8 -*-
from acid import db
from acid.app import app


class TestWithAppContext:
    def setup_method(self, method):
        self._ctx = app.app_context()
        self._ctx.push()

    def teardown_method(self, method):
        self._ctx.pop()


class DatabaseTestCase:
    def setup_method(self, method):
        try:
            db.db.bind(provider='sqlite', filename=':memory:')
            db.db.generate_mapping(create_tables=True)
        except TypeError:
            pass

    def teardown_method(self, method):
        db.db.drop_all_tables(with_all_data=True)
        db.db.create_tables()


class IntegrationTestCase(TestWithAppContext, DatabaseTestCase):
    def setup_method(self, method):
        TestWithAppContext.setup_method(self, method)
        DatabaseTestCase.setup_method(self, method)

    def teardown_method(self, method):
        DatabaseTestCase.teardown_method(self, method)
        TestWithAppContext.teardown_method(self, method)
