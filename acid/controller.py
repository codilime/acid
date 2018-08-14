# -*- coding: utf-8 -*-
import requests

from flask import Blueprint

from acid.error_handler import ErrorHandler, bind_error_handlers
from acid.features.history.exceptions import PageOutOfRange
from acid.features.status.exceptions import (BadDataFormat, PipelineNotFound,
                                             RemoteServerError)

error_handlers = Blueprint('error_handlers', __name__,
                           template_folder='templates/errors')


handlers = [
    ErrorHandler([BadDataFormat, RemoteServerError, Exception], 'error.html',
                 requests.codes.server_error),
    ErrorHandler([PipelineNotFound, PageOutOfRange, 404], 'error_404.html',
                 requests.codes.not_found),
]

bind_error_handlers(error_handlers, handlers)
