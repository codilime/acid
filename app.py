# -*- coding: utf-8 -*-
from flask import Flask

from dashboard.controller import builds, error_handlers, status

app = Flask(__name__)

app.url_map.strict_slashes = False

app.register_blueprint(error_handlers)
app.register_blueprint(status)
app.register_blueprint(builds)
