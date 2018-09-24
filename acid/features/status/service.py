# -*- coding: utf-8 -*-
import requests

from flask import current_app

from .exceptions import PipelineNotFound, RemoteServerError
from .model import PipelineStat, Queue


def fetch_json_data(endpoint):
    res = requests.get(endpoint, timeout=3)

    if res.status_code not in [200, 304]:
        current_app.logger.error(res.text)
        raise RemoteServerError('Request for Zuul status failed.')

    return res.json()


def pipelines_stats(pipelines, showed_pipelines):
    if not showed_pipelines:
        return []

    pipeline_stats = []
    for pipeline in pipelines:
        if pipeline['name'] in showed_pipelines:
            buildsets_count = 0
            for queue in pipeline['change_queues']:
                heads = queue.get('heads')
                if heads:
                    buildsets_count += len(heads[0])
            pipeline_stats.append(PipelineStat(name=pipeline['name'],
                                               buildsets_count=buildsets_count))
    return pipeline_stats


def get_zuul_pipelines():
    config = current_app.config
    zuul_url = config['zuul']['url']
    zuul_endpoint = config['zuul']['status_endpoint']

    url = status_endpoint(zuul_url, zuul_endpoint)
    return fetch_json_data(endpoint=url)['pipelines']


def pipelines_intersection(pipelines_config, pipelines_json):
    if not pipelines_config or not pipelines_json:
        return []

    pipelines_to_show = [pipeline['name'] for pipeline in pipelines_json
                         if pipeline['name'] in pipelines_config]
    return pipelines_to_show


def get_pipelines():
    config = current_app.config
    return pipelines_intersection(config['zuul']['pipelines'], get_zuul_pipelines())


def make_queues(pipelines, pipename, zuul_url):
    for pipeline in pipelines:
        if pipeline['name'] == pipename:
            return [Queue.create(q, zuul_url)
                    for q in pipeline['change_queues']]
    else:
        current_app.logger.error(f'Pipe "{pipename}" not found.')
        raise PipelineNotFound(f'Pipe "{pipename}" not found.')


def status_endpoint(zuul_url, zuul_endpoint):
    return str(f'{zuul_url.rstrip("/")}/{zuul_endpoint}')
