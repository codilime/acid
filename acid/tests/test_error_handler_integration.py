# -*- coding: utf-8 -*-

from unittest.mock import patch

import pytest

import requests

from acid.app import app
from acid.controller import error_handlers
from acid.error_handler import ErrorHandler, bind_error_handlers
from acid.features.history.exceptions import PageOutOfRange
from acid.tests import IntegrationTestCase


@patch('acid.db.connect')
class TestErrorHandlerIntegration(IntegrationTestCase):

    @pytest.mark.integration
    def test_client_uses_binded_error_handler(self, _):
        handlers = [ErrorHandler([PageOutOfRange],
                                 'error_404.html',
                                 requests.codes.im_a_teapot)]

        bind_error_handlers(error_handlers, handlers)

        self._update_blueprint()

        with app.test_client() as client:
            rv = client.get('/builds/144')

        self.assertEqual(requests.codes.im_a_teapot, rv.status_code)

    @staticmethod
    def _update_blueprint():
        app.blueprints = {}
        app.register_blueprint(error_handlers)
