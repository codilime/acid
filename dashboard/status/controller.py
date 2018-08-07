from flask import render_template, Blueprint

from dashboard.status import service
from dashboard.config import config


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
    return render_template('dashboard.html', pipeline_stats=pipeline_stats)
