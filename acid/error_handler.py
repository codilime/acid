# -*- coding: utf-8 -*-

from typing import List, NamedTuple, Type

from flask import current_app, make_response, render_template, request


class ErrorHandler(NamedTuple):
    exceptions: List[Type[Exception]]  # noqa
    template_file: str
    error_code: int


def bind_error_handlers(error_handlers_blueprint,
                        error_handlers: List[ErrorHandler]):
    """
    Wrapper of app_errorhandler for blueprints
    to provide more comprehensive API
    """
    for handler in error_handlers:
        for exception in handler.exceptions:
            callback = _error_handler_callback(handler.template_file,
                                               handler.error_code)
            error_handlers_blueprint.app_errorhandler(exception)(callback)


def _error_handler_callback(template, error_code):
    def decorator(error):
        current_app.logger.exception(f'{error}; raised on URL: {request.url}')
        return make_response(render_template(template), error_code)

    return decorator
