# -*- coding: utf-8 -*-
import logging.handlers
import os
import errno


def pipe_intersect(pipelines_config, pipelines_json):
    if not pipelines_config or not pipelines_json:
        return []

    return [pipeline['name'] for pipeline in pipelines_json
            if pipeline['name'] in pipelines_config]


def get_logger(feature_name=None):
    if feature_name:
        return logging.getLogger(feature_name)
    else:
        return logging.getLogger('acid')


class FileCreatorHandler(logging.handlers.WatchedFileHandler):
    def __init__(self, filename, mode='a', encoding=None, delay=0):
        try:
            os.makedirs(os.path.dirname(filename), exist_ok=True)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        super().__init__(filename, mode, encoding, delay)
