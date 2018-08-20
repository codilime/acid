# -*- coding: utf-8 -*-
import os


def path_to_test_file(filename):
    rootdir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(rootdir, 'static', filename)
