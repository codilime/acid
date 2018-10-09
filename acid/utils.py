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
        try:
            config[plugin_name].update(settings)
        except KeyError:
            config[plugin_name] = settings
    return config


# load features configuration from all files
def load_plugin_configs():
    conf_dirs = ['history.d', 'manager.d', 'status.d']
    conf_root = 'config'

    config = {}

    for _dir in conf_dirs:
        _files = os.listdir('/'.join([conf_root, _dir]))
        _files = ['/'.join([conf_root, _dir, f]) for f in _files
                  if f.endswith('.yml')]

        for _file in _files:
            try:
                # load configuration from file
                settings = load_configuration_file(_file)
                for _plugin in settings.keys():
                    # create plugin key if it doesn't exist
                    if _plugin not in config:
                        config[_plugin] = {}
                    # update features configuration in plugin
                    config[_plugin].update(settings[_plugin])
            except IOError as e:
                print(f'Can\'t read file {_file}')
                print(e)
    return config


# load configuration from one file
def load_configuration_file(file):
    # read yaml file
    print(f'Reading configuration file: {file}')
    settings = read_yaml(file_path=os.path.normpath(file))
    # get plugins configs
    settings = settings.get('plugin', {})

    config = {}

    # create dictionary entry for each plugin and feature in file
    for _plugin, _features in settings.items():
        for _feature, _feat_conf in _features.items():
            if _plugin not in config:
                config[_plugin] = {}

            config[_plugin][_feature] = _feat_conf

    return config


def load_feature_conf(name, whole_config):
    for plugin, features in whole_config.items():
        for feature, configuration in features.items():
            if feature == name:
                config = {feature: configuration}
                return config, plugin

    print(f'Couldn\'t find configuration for feature: {name}')
    return {}, None
