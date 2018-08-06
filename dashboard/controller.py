# -*- coding: utf-8 -*-
from flask import (Blueprint, current_app, redirect, render_template, request,
                   url_for)

from pony.orm import db_session

from dashboard import db, service
from dashboard.config import config
from dashboard.exceptions import (AuthenticationFailed, BadDataFormat,
                                  PageOutOfRange, PipelineNotFound,
                                  RemoteServerError)
from dashboard.history import BuildSetsFiltered, BuildSetsPaginated, pagination

status = Blueprint('status', __name__, template_folder='templates')
builds = Blueprint('builds', __name__, template_folder='templates')
auth = Blueprint('auth', __name__, template_folder='templates')
error_handlers = Blueprint('error_handlers', __name__,
                           template_folder='templates/errors')


@error_handlers.app_errorhandler(BadDataFormat)
@error_handlers.app_errorhandler(RemoteServerError)
@error_handlers.app_errorhandler(Exception)
def generic_error(error):
    current_app.logger.error(f"{error}; raised on URL: {request.url}")
    return render_template('error.html')


@error_handlers.app_errorhandler(PipelineNotFound)
@error_handlers.app_errorhandler(PageOutOfRange)
@error_handlers.app_errorhandler(404)
def error_404(error):
    current_app.logger.error(f"{error}; raised on URL: {request.url}")
    return render_template('error_404.html')


@error_handlers.app_errorhandler(AuthenticationFailed)
def auth_error(error):
    current_app.logger.error(f"{error}; raised on URL: {request.url}")
    return render_template('auth_error.html')


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


@builds.route('/builds')
@builds.route('/builds/<int:page>')
@db_session
def show_builds_history(page=1):
    per_page = config['buildset']['per_page']
    pipeline = config['default']['pipename']
    page_links = config['buildset']['page_links']
    buildset_log_url = config['buildset']['log_url']

    db.connect()

    branch = request.args.get('branch')
    build = request.args.get('build')

    if branch or build:
        buildsets = BuildSetsFiltered(pipeline, per_page, branch, build)
    else:
        buildsets = BuildSetsPaginated(pipeline, per_page)

    buildsets.fetch_page(page)
    paginator = pagination(len(buildsets), page, per_page, page_links)
    return render_template('builds_history.html', buildsets=buildsets,
                           paginator=paginator,
                           buildsets_log_url=buildset_log_url)


@auth.route('/sign_in')
def sign_in():
    redirect_url = service.start_openid_auth()
    return redirect(redirect_url)


@auth.route('/signed_in')
def signed_in():
    user = service.fetch_user_data()
    service.create_user_session(user)
    return redirect(url_for('status.show_dashboard'))


@auth.route('/sign_out')
def sign_out():
    service.drop_user_session()
    return redirect(url_for('status.show_dashboard'))
