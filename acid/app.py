# -*- coding: utf-8 -*-
import os
import logging.config

from flask import Flask

from flask_session import Session

from acid.yaml_utils import read_yaml
from acid.controller import error_handlers
from acid.features.auth.controller import auth
from acid.features.auth.model import get_current_user
from acid.features.history.controller import builds
from acid.features.status.controller import status
from acid.features.status.service import get_zuul_pipelines
from acid.utils import pipe_intersect
from acid.features.zuul_manager.controller import zuul_manager
from acid.features.zuul_manager_v2.controller import zuul_manager_v2

if os.getenv('FLASK_ENV') == 'production' and not os.getenv('SECRET_KEY'):
    raise Exception("On production use environment variables")

app = Flask(__name__, static_folder='../static')

settings = read_yaml(file_path=os.path.normpath(os.getenv('SETTINGS_PATH')))
app.config.update(settings)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY',
                                     app.config['default']['secret_key'])
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False

logging.config.fileConfig('config/logging.conf')
Session(app)

app.url_map.strict_slashes = False

app.register_blueprint(error_handlers)
app.register_blueprint(status)
app.register_blueprint(builds)
app.register_blueprint(auth)
app.register_blueprint(zuul_manager)
app.register_blueprint(zuul_manager_v2)


@app.context_processor
def template_context():
    return {'pipeline_names': pipe_intersect(app.config['zuul']['pipelines'],
                                             get_zuul_pipelines()),
            'current_user': get_current_user()}
