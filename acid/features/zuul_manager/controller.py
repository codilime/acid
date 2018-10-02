# -*- coding: utf-8 -*-
import requests

from flask import (Blueprint, abort, current_app, flash, redirect,
                   render_template, request, url_for)

from ..auth.service import admin_required
from .manager import ZuulManager

zuul_manager = Blueprint('zuul_manager', __name__,
                         template_folder='../../templates')


@zuul_manager.route('/zuul_manager')
@admin_required
def show_panel():
    config_pipelines = current_app.config['zuul']['build_enqueue']['pipelines']

    pipelines_arg = request.args.getlist('pipeline')
    branches_arg = request.args.getlist('branch')

    pipelines = config_pipelines

    # add pipeline filtering
    if pipelines_arg:
        pipelines = {pipeline: branches for pipeline, branches
                     in pipelines.items() if pipeline in pipelines_arg}

    # add branch filtering
    if branches_arg:
        pipelines = {k: [v2 for v2 in v if v2 in branches_arg]
                     for k, v in pipelines.items()}

    branches_list = set([i for v in config_pipelines.values() for i in v])

    return render_template('zuul_manager.html', pipelines=pipelines,
                           pipelines_list=config_pipelines,
                           branches_list=branches_list)


@zuul_manager.route('/zuul_manager/manage', methods=['POST'])
@admin_required
def manage():
    pipeline_name = request.form.get('pipeline_name')
    branch = request.form.get('branch')
    action = request.form.get('action')

    zuul_manager = ZuulManager(**current_app.config['zuul']['manager'])

    pipelines = current_app.config['zuul']['build_enqueue']['pipelines']
    if pipeline_name not in pipelines.keys():
        abort(requests.codes.bad_request)
    if branch not in pipelines[pipeline_name]:
        abort(requests.codes.bad_request)

    if action == 'start':
        zuul_manager.enqueue(pipeline_name, branch)
    elif action == 'stop':
        zuul_manager.dequeue(pipeline_name, branch)
    else:
        abort(requests.codes.bad_request)

    flash('Job started. It might take a while for zuul to update', 'info')
    return redirect(url_for('status.show_status', pipename=pipeline_name))
