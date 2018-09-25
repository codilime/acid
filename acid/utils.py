# -*- coding: utf-8 -*-


def pipe_intersect(pipelines_config, pipelines_json):
    if not pipelines_config or not pipelines_json:
        return []

    pipelines_to_show = [pipeline['name'] for pipeline in pipelines_json
                         if pipeline['name'] in pipelines_config]
    return pipelines_to_show
