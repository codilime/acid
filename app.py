# -*- coding: utf-8 -*-
from flask import Flask

from dashboard.controller import builds, status

app = Flask(__name__)
app.register_blueprint(status)
app.register_blueprint(builds)
