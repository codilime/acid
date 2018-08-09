# -*- coding: utf-8 -*-
import requests

from flask import (Blueprint, current_app,
                   make_response, render_template, request)

from dashboard.status.exceptions import (BadDataFormat,
                                         PipelineNotFound,
                                         RemoteServerError)
from dashboard.history.exceptions import PageOutOfRange

error_handlers = Blueprint('error_handlers', __name__,
                           template_folder='templates/errors')


@error_handlers.app_errorhandler(BadDataFormat)
@error_handlers.app_errorhandler(RemoteServerError)
@error_handlers.app_errorhandler(Exception)
def generic_error(error):
    current_app.logger.error(f'{error}; raised on URL: {request.url}')
    return make_response(render_template('error.html'),
                         requests.codes.server_error)


@error_handlers.app_errorhandler(PipelineNotFound)
@error_handlers.app_errorhandler(PageOutOfRange)
@error_handlers.app_errorhandler(404)
def error_404(error):
    current_app.logger.error(f'{error}; raised on URL: {request.url}')
    return make_response(render_template('error_404.html'),
                         requests.codes.not_found)
