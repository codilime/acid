# -*- coding: utf-8 -*-
from flask import Blueprint, current_app, render_template, request

from pony.orm import db_session

from acid import db

from .service import BuildSetsFiltered, BuildSetsPaginated, pagination

builds = Blueprint('builds', __name__, template_folder='../../templates')


@builds.route('/builds')
@builds.route('/builds/<int:page>')
@db_session
def show_builds_history(page=1):
    per_page = current_app.config['buildset']['per_page']
    pipeline = current_app.config['default']['pipename']
    page_links = current_app.config['buildset']['page_links']
    buildset_log_url = current_app.config['buildset']['log_url']

    db.connect()

    branches =  request.args.getlist('branch')
    build = request.args.get('build')

    if branches or build:
        buildsets = BuildSetsFiltered(pipeline, per_page, branches, build)
    else:
        buildsets = BuildSetsPaginated(pipeline, per_page)
    buildsets.fetch_page(page)
    paginator = pagination(len(buildsets), page, per_page, page_links)
    return render_template('builds_history.html', buildsets=buildsets,
                           paginator=paginator,
                           buildsets_log_url=buildset_log_url,
                           branches=branches)
