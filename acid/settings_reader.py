# -*- coding: utf-8 -*-
import os

import yaml


def read_yaml(file_path):
    if not isinstance(file_path, (str, os.PathLike, bytes)):
        raise TypeError(f'expected str, bytes or os.PathLike object, '
                        f'not {type(file_path).__name__}')

    with open(os.path.normpath(file_path), 'r') as f:
        conf = yaml.safe_load(f)
    return conf
