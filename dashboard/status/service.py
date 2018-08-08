# -*- coding: utf-8 -*-
import requests

from flask import current_app

from dashboard.config import config
from dashboard.status.exceptions import PipelineNotFound, RemoteServerError
from dashboard.status.model import PipelineStat, Queue


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
