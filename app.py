# -*- coding: utf-8 -*-
import os

from flask import Flask

from flask_session import Session

from dashboard.config import config
from dashboard.controller import error_handlers
from dashboard.auth.controller import auth
from dashboard.history.controller import builds
from dashboard.status.controller import status

if os.getenv('FLASK_ENV') == 'production' and not os.getenv('SECRET_KEY'):
    raise Exception("On production use environment variables")

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY',
                                     config['default']['secret_key'])
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
Session(app)

app.url_map.strict_slashes = False

app.register_blueprint(error_handlers)
app.register_blueprint(status)
app.register_blueprint(builds)
app.register_blueprint(auth)


@app.context_processor
def template_context():
    return {'pipelines': config['zuul']['pipelines']}
