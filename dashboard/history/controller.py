# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request

from pony.orm import db_session

from dashboard import db
from dashboard.config import config
from dashboard.history.service import (BuildSetsFiltered,
                                       BuildSetsPaginated,
                                       pagination)

builds = Blueprint('builds', __name__, template_folder='../templates')


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
