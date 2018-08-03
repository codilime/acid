# -*- coding: utf-8 -*-
import urllib.parse

import requests

from flask import current_app, request, session, url_for

from openid.consumer import consumer
from openid.extensions import sreg

from dashboard.config import config
from dashboard.exceptions import (AuthenticationFailed, PipelineNotFound,
                                  RemoteServerError)
from dashboard.status import PipelineStat, Queue
from dashboard.users import User


def fetch_json_data(endpoint):
    res = requests.get(endpoint, timeout=3)

    if res.status_code not in [200, 304]:
        current_app.logger.error(res.text)
        raise RemoteServerError('Request for Zuul status failed.')

    return res.json()


def pipelines_stats(pipelines):
    pipeline_stats = []
    for pipeline in pipelines:
        if pipeline['name'] in config['zuul']['pipelines']:
            buildsets_count = 0
            for queue in pipeline['change_queues']:
                heads = queue.get('heads')
                if heads:
                    buildsets_count += len(heads[0])
            pipeline_stats.append(PipelineStat(name=pipeline['name'],
                                               buildsets_count=buildsets_count))
    return pipeline_stats


def make_queues(pipelines, pipename):
    for pipeline in pipelines:
        if pipeline['name'] == pipename:
            return [Queue.create(q) for q in pipeline['change_queues']]
    else:
        current_app.logger.error(f'Pipe "{pipename}" not found.')
        raise PipelineNotFound(f'Pipe "{pipename}" not found.')


def status_endpoint():
    return str(f'{config["zuul"]["url"].rstrip("/")}/'
               f'{config["zuul"]["status_endpoint"]}')


def create_user_session(user):
    session['user'] = user


def drop_user_session():
    session.pop('user')


def fetch_user_data():
    # (kam193) OpenID library needs full decoded url, but from flask we
    # can get only encoded URL which breaks parsing.
    full_decoded_url = urllib.parse.urljoin(request.host_url, request.full_path)

    oid_consumer = consumer.Consumer(session, None)
    info = oid_consumer.complete(request.args, full_decoded_url)
    if info.status != consumer.SUCCESS:
        error_message = getattr(info, 'message', '<no detail information>')
        raise AuthenticationFailed(f"Sign in failed. Status: {info.status}, "
                                   f"message: {error_message}")

    user_data = sreg.SRegResponse.fromSuccessResponse(info)
    return User(full_name=user_data['fullname'], email=user_data['email'])


def start_openid_auth():
    oid_consumer = consumer.Consumer(session, None)
    oid_request = oid_consumer.begin(config['default']['openid_provider'])

    user_data_request = sreg.SRegRequest(required=['email', 'fullname'])
    oid_request.addExtension(user_data_request)

    return_to = url_for('auth.signed_in', _external=True)
    return oid_request.redirectURL(request.url_root, return_to=return_to)
