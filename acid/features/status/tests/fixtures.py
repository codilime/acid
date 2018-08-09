# -*- coding: utf-8 -*-
from os import path
from json import load
from random import randint
from unittest.mock import MagicMock

from acid.config import config
from acid.status.model import Buildset, Job, TimeTracker


def time_tracker():
    return TimeTracker(start=randint(1000, 100000),  # noqa
                       elapsed=randint(1000, 100000),  # noqa
                       remaining=randint(1000, 100000),  # noqa
                       estimated=randint(1000, 100000))  # noqa


def job():
    return Job(name="test_name", result="test_result",
               url="http://fake_url", report_url="http://fake_url",
               canceled=False, voting=False, retry=False,
               worker={"name": "fake_name"},
               time_tracker=time_tracker())


def buildset():
    return Buildset(name="test_name", buildset_id="12345,6", jobs=[],
                    enqueue_time=randint(1000, 100000),  # noqa
                    owner={'name': 'John smith'}, ref='12345',
                    review_url="http://fake_url")


def status_request(filename=None, status_code=200):
    current_dir = path.dirname(path.realpath(__file__))
    filename = filename or config['zuul']['status_endpoint']
    result = MagicMock()
    result.status_code = status_code
    with open(f'{current_dir}/static/{filename}.json') as json_data:
        result.json = MagicMock(return_value=load(json_data))
    return MagicMock(return_value=result)


def load_status_data(name):
    current_dir = path.dirname(path.realpath(__file__))
    with open(f'{current_dir}/static/{name}.json', "r") as data:
        return load(data)
