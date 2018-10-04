# -*- coding: utf-8 -*-
import os

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

if os.getenv('FLASK_ENV') == 'production' and not os.getenv('SECRET_KEY'):
    raise Exception("On production use environment variables")

app = Flask(__name__, static_folder='../static')

settings = read_yaml(file_path=os.path.normpath(f'config/core_settings.yml'))
app.config.update(settings)

feats = read_yaml(file_path=os.path.normpath(f'config/feature_conf.yml'))

for feature in feats['ACID']:
    for _type, _conf in feature.items():
        try:
            settings = read_yaml(file_path=os.path.normpath(f'config/{_conf}'))
            print(f'Reading configuration file: {_conf}')
            try:
                app.config[_type].update(settings[_type])
            except KeyError as e:
                app.config.update(settings)
        except FileNotFoundError as e:
            print(f'Can\'t read file {_conf}')
            print(e)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY',
                                     app.config['default']['secret_key'])
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False

Session(app)

app.url_map.strict_slashes = False

app.register_blueprint(error_handlers)
app.register_blueprint(status)
app.register_blueprint(builds)
app.register_blueprint(auth)
app.register_blueprint(zuul_manager)


@app.context_processor
def template_context():
    return {'pipeline_names': pipe_intersect(app.config['status']['pipelines'],
                                             get_zuul_pipelines()),
            'current_user': get_current_user()}
