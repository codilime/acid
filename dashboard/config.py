# -*- coding: utf-8 -*-
import os
from configparser import ConfigParser, ExtendedInterpolation

config = ConfigParser(interpolation=ExtendedInterpolation())
config.read(os.path.normpath(os.getenv('SETTINGS_PATH')))
