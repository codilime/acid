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
    if not pipelines or not showed_pipelines:
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
    config = current_app.config['status']['status']
    zuul_url = config['url']
    zuul_endpoint = config['status_endpoint']
    url = status_endpoint(zuul_url, zuul_endpoint)

    try:
        result = fetch_json_data(endpoint=url).get('pipelines')
    except RemoteServerError:
        print("Couldn't fetch .json file")
        result = []
    return result


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
