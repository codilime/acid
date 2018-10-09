# -*- coding: utf-8 -*-
import requests

from flask import (Blueprint, abort, current_app, flash, redirect,
                   render_template, request, url_for)

from ..auth.service import admin_required
from .manager import ZuulManager

zuul_manager = Blueprint('zuul_manager', __name__,
                         template_folder='../../templates')


@zuul_manager.route('/zuul_manager')
@zuul_manager.route('/zuul_manager/<string:feature>')
@admin_required
def show_panel(feature=''):
    pipelines = current_app.config['zuul_manager'][feature]['pipelines']
    return render_template('zuul_manager.html', pipelines=pipelines)


@zuul_manager.route('/zuul_manager/manage', methods=['POST'])
@zuul_manager.route('/zuul_manager/<string:feature>/manage', methods=['POST'])
@admin_required
def manage(feature='my_manager'):
    pipeline_name = request.form.get('pipeline_name')
    branch = request.form.get('branch')
    action = request.form.get('action')

    zuul_manager = ZuulManager(**current_app.config['zuul_manager'][feature])

    for pipeline in current_app.config['zuul_manager'][feature]['pipelines']:
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

        flash('Job started. It might take a while for zuul to update', 'info')
        return redirect(url_for('status.show_status', pipename=pipeline_name))
    abort(requests.codes.bad_request)
