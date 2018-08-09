# -*- coding: utf-8 -*-
import os

import yaml


class Config:
    """App config abstraction.

    Config object is a wrapper around dictionary produced by YAML parser.
    It's main goal is to provide separation between config file format
    and config object interface.
    Second goal is to provide a way to load more than one config if needed.
    Can be easily extend to provide more format files
    by overloading _load() method.
    """

    def __init__(self, file_path):
        if not isinstance(file_path, (str, os.PathLike, bytes)):
            raise TypeError(f'expected str, bytes or os.PathLike object, '
                            f'not {type(file_path).__name__}')
        self.file_path = file_path
        self._conf = self._load()

    def __repr__(self):
        return repr(self._conf)

    def __getitem__(self, item):
        return self._conf[item]

    def __contains__(self, item):
        return self._conf.__contains__(item)

    def __getattr__(self, item):
        try:
            return getattr(self._conf, item)
        except AttributeError:
            # Pack up attribute error from _conf dict
            # to be shown as config object attribute error.
            raise AttributeError(f'"{self.__class__.__name__}" '
                                 f'has no attribute {item}') from None

    def _load(self) -> dict:
        with open(os.path.normpath(self.file_path), 'r') as f:
            conf = yaml.safe_load(f)
        return conf


config = Config(file_path=os.path.normpath(os.getenv('SETTINGS_PATH')))
