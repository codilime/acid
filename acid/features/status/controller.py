# -*- coding: utf-8 -*-
from flask import Blueprint, render_template

from acid.status import service
from acid.config import config


status = Blueprint('status', __name__, template_folder='templates')


@status.route('/status')
@status.route('/status/<string:pipename>')
def show_status(pipename=config['default']['pipename']):
    url = service.status_endpoint()
    resource = service.fetch_json_data(endpoint=url)
    queues = service.make_queues(resource['pipelines'], pipename)
    return render_template('status.html', queues=queues, pipename=pipename)


@status.route('/')
def show_dashboard():
    url = service.status_endpoint()
    resource = service.fetch_json_data(endpoint=url)
    pipeline_stats = service.pipelines_stats(resource['pipelines'])
    return render_template('acid.html', pipeline_stats=pipeline_stats)
