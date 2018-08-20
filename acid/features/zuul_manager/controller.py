# -*- coding: utf-8 -*-
import requests

from flask import Blueprint, abort, redirect, render_template, request, url_for

from acid.config import config

from ..auth.service import login_required
from .manager import ZuulManager

zuul_manager = Blueprint('zuul_manager', __name__,
                         template_folder='../../templates')


@zuul_manager.route('/zuul_manager')
@login_required
def show_panel():
    pipelines = config['zuul']['build_enqueue']['pipelines']
    return render_template('zuul_manager.html', pipelines=pipelines)


@zuul_manager.route('/zuul_manager/manage', methods=['POST'])
@login_required
def manage():
    pipeline_name = request.form.get('pipeline_name')
    branch = request.form.get('branch')
    action = request.form.get('action')

    zuul_manager = ZuulManager(**config['zuul']['manager'])

    for pipeline in config['zuul']['build_enqueue']['pipelines']:
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