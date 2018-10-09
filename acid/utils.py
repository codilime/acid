# -*- coding: utf-8 -*-
from acid.yaml_utils import read_yaml

import os


def pipe_intersect(pipelines_config, pipelines_json):
    if not pipelines_config or not pipelines_json:
        return []

    return [pipeline['name'] for pipeline in pipelines_json
            if pipeline['name'] in pipelines_config]


def prepare_features(features, whole_config):
    config = {}

    for feature in features['ACID']:
        settings, plugin_name = load_feature_conf(feature, whole_config)
        # settings = read_yaml(file_path=os.path.normpath(f'config/{_conf}'))
        try:
            config[plugin_name].update(settings)
        except KeyError:
            config[plugin_name] = settings
    # for k, v in config.items():
        # print(f'{k}: {v}')
        # print()
    return config


def load_configurations():
    conf_dirs = ['auth.d', 'history.d', 'manager.d', 'status.d']
    conf_root = 'config'

    config = {'plugin': {}, 'core': {}}

    for _dir in conf_dirs:
        _files = os.listdir('/'.join([conf_root, _dir]))
        _files = ['/'.join([conf_root, _dir, f]) for f in _files
                  if f.endswith('.yml')]

        for _file in _files:
            try:
                settings = read_yaml(file_path=os.path.normpath(_file))
                print(f'Reading configuration file: {_file}')

                for _type, _conf in settings.items():
                    if _type == 'plugin':
                        for _feature, _feat_conf in _conf.items():
                            try:
                                config[_type][_feature].update(settings[_type][_feature])
                            except KeyError:
                                config[_type].update(settings['plugin'])
            except IOError as e:
                print(f'Can\'t read file {_file}')
                print(e)
    return config


def load_feature_conf(name, whole_config):
    # print(name)
    for plugin, features in whole_config['plugin'].items():
        for feature, configuration in features.items():
            if feature == name:
                # print(f'Feature: {name} found in: {plugin}')
                config = {name: whole_config['plugin'][plugin][name]}
                # print(config)
                return config, plugin

    print(f'Couldn\'t find configuration for feature: {name}')
    return {}, None
