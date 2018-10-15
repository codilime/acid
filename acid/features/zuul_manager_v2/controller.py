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
    config_pipelines = current_app.config['zuul']['build_enqueue']['pipelines']

    pipelines_arg = request.args.getlist('pipeline')
    branches_arg = request.args.getlist('branch')

    pipelines = config_pipelines

    if pipelines_arg:
        pipelines = {pipe: branches for pipe, branches
                     in pipelines.items() if pipe in pipelines_arg}

    if branches_arg:
        pipelines = {pipe: [branch for branch in branches
                            if branch in branches_arg]
                     for pipe, branches in pipelines.items()}

    branches_list = {branch for branches in config_pipelines.values()
                     for branch in branches}

    return render_template('zuul_manager_v2.html', pipelines=pipelines,
                           pipelines_arg=pipelines_arg,
                           branches_arg=branches_arg,
                           pipelines_list=config_pipelines,
                           branches_list=branches_list)


@zuul_manager_v2.route('/zuul_manager_v2/manage', methods=['POST'])
@admin_required
def manage():
    pipeline_name = request.form.get('pipeline_name')
    branch = request.form.get('branch')
    action = request.form.get('action')

    zuul_manager = ZuulManager(**current_app.config['zuul']['manager_v2'])

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

    return redirect(url_for('status.show_status', pipename=pipeline_name))
