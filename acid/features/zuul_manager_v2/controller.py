# -*- coding: utf-8 -*-
import requests

from flask import (Blueprint, abort, current_app, redirect,
                   render_template, request, url_for)

from ..auth.service import admin_required
from .manager import ZuulManager

zuul_manager_v2 = Blueprint('zuul_manager_v2', __name__,
                         template_folder='../../templates')


@zuul_manager_v2.route('/zuul_manager_v2')
@admin_required
def show_panel():
    pipelines = current_app.config['zuul']['build_enqueue']['pipelines']
    return render_template('zuul_manager_v2.html', pipelines=pipelines)


@zuul_manager_v2.route('/zuul_manager_v2/manage', methods=['POST'])
@admin_required
def manage():
    pipeline_name = request.form.get('pipeline_name')
    branch = request.form.get('branch')
    action = request.form.get('action')

    zuul_manager = ZuulManager(**current_app.config['zuul']['manager_v2'])

    for pipeline in current_app.config['zuul']['build_enqueue']['pipelines']:
        if pipeline_name not in pipeline.keys():
            continue
        if branch not in pipeline[pipeline_name]:
            continue

        if action == 'start':
            zuul_manager.enqueue(pipeline_name, branch)
        elif action == 'stop':
            zuul_manager.dequeue(pipeline_name, branch)
        else:
            abort(requests.codes.bad_request)

        return redirect(url_for('status.show_status', pipename=pipeline_name))
    abort(requests.codes.bad_request)
