# -*- coding: utf-8 -*-
import inspect
from typing import Callable
from unittest import mock
from unittest.mock import call

import pytest

from acid.controller import error_handlers
from acid.error_handler import ErrorHandler, bind_error_handlers
from acid.features.history.exceptions import PageOutOfRange
from acid.features.status.exceptions import RemoteServerError


@pytest.mark.unit
def test_blueprint_register_callbacks(monkeypatch, mocker):
    callback_mock = mock.MagicMock()
    monkeypatch.setattr(error_handlers, 'app_errorhandler',
                        lambda _: callback_mock)
    mocker.spy(error_handlers, 'app_errorhandler')

    handlers = [
        ErrorHandler([Exception, RemoteServerError], 'generic.html', 500),
        ErrorHandler([PageOutOfRange], '404.html', 404)
    ]

    bind_error_handlers(error_handlers_blueprint=error_handlers,
                        error_handlers=handlers)

    assert error_handlers.app_errorhandler.call_args_list == [
        call(Exception), call(RemoteServerError), call(PageOutOfRange)]

    assert callback_mock.call_args_list == [call(ErrorHandlerCallback)] * 3


class _ErrorHandlerCallback(object):
    def __eq__(self, other):
        if not isinstance(other, Callable):
            return False
        try:
            inspect.signature(other).bind('error')
        except TypeError:
            return False
        return True


ErrorHandlerCallback = _ErrorHandlerCallback()
