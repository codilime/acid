# -*- coding: utf-8 -*-
import requests

from flask import Blueprint, abort, redirect, render_template, request, url_for

from acid.config import config

from ..auth.model import get_current_user
from . import service

zuul_manager = Blueprint('zuul_manager', __name__,
                         template_folder='../../templates')


@zuul_manager.route('/zuul_manager')
def show_panel():
    current_user = get_current_user()
    if not current_user or not current_user.is_admin():
        abort(requests.codes.unauthorized)

    pipelines = config['zuul']['build_enqueue']['pipelines']
    return render_template('zuul_manager.html', pipelines=pipelines)


@zuul_manager.route('/zuul_manager/manage', methods=['POST'])
def manage():
    current_user = get_current_user()
    if not current_user or not current_user.is_admin():
        abort(requests.codes.unauthorized)

    pipeline_name = request.form.get('pipeline_name')
    branch = request.form.get('branch')
    action = request.form.get('action')

    for pipeline in config['zuul']['build_enqueue']['pipelines']:
        if pipeline_name not in pipeline.keys():
            continue
        if branch not in pipeline[pipeline_name]:
            continue

        if action == 'start':
            service.start_buildset(pipeline_name, branch)
        elif action == 'stop':
            service.stop_buildset(pipeline_name, branch)
        else:
            abort(requests.codes.bad_request)

        return redirect(url_for('status.show_status', pipename=pipeline_name))
    abort(requests.codes.bad_request)
