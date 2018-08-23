# -*- coding: utf-8 -*-
from acid import db
from acid.app import app


class TestWithAppContext:
    def setup_method(self, method):
        self._ctx = app.app_context()
        self._ctx.push()

    def teardown_method(self, method):
        self._ctx.pop()


class IntegrationTestCase(TestWithAppContext):
    def setup_method(self, method):
        super().setup_method(method)
        db.connect()

    def teardown_method(self, method):
        db.db.disconnect()
        super().teardown_method(method)


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
