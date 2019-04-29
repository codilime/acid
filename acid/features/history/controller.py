# -*- coding: utf-8 -*-
from datetime import datetime

from flask import Blueprint, Response, current_app, render_template, request

from pony.orm import db_session

from acid import db

from .service import BuildSetsPaginated, pagination

builds = Blueprint('builds', __name__, template_folder='../../templates')


@builds.route('/builds')
@builds.route('/builds/<int:page>')
@db_session
def show_builds_history(page=1):
    config = current_app.config
    per_page = config['history']['pagination']['per_page']
    pipeline = config['default']['pipename']
    page_links = config['history']['pagination']['page_links']
    buildset_log_url = config['history']['log_server_url']
    max_latest_ref_count = config['history'].get(
        'max_latest_ref_count', 200)

    db.connect()

    refs = request.args.getlist('refs')
    build = request.args.get('build', '')
    download_json = request.args.get('json', '')
    limit = request.args.get('limit', 0)

    buildsets = BuildSetsPaginated(
        pipeline, max_latest_ref_count, per_page, refs, build)

    if download_json == 'True':
        json_result = buildsets.to_json(limit)
        filename = f'builds_history_{datetime.now().isoformat()}.json'
        disposition = f'attachment;filename={filename}'
        return Response(json_result, mimetype='application/json',
                        headers={'Content-Disposition': disposition})

    buildsets_len = len(buildsets)
    buildsets.fetch_page(page)
    paginator = pagination(buildsets_len, page, per_page, page_links)
    template = render_template('builds_history.html', buildsets=buildsets,
                               paginator=paginator,
                               buildsets_log_url=buildset_log_url,
                               refs=refs)
    return template
