# -*- coding: utf-8 -*-
import logging


def pipe_intersect(pipelines_config, pipelines_json):
    if not pipelines_config or not pipelines_json:
        return []

    return [pipeline['name'] for pipeline in pipelines_json
            if pipeline['name'] in pipelines_config]


def get_feature_logger(feature_name=None):
    if feature_name:
        return logging.getLogger(feature_name.replace('acid.features.', ''))
    else:
        return logging.getLogger(None)
