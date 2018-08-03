# -*- coding: utf-8 -*-
import json
import random
from unittest.mock import MagicMock

from dashboard.config import config
from dashboard.status import Buildset, Job, TimeTracker
from dashboard.users import User


def time_tracker():
    return TimeTracker(start=random.randint(1000, 100000),  # noqa
                       elapsed=random.randint(1000, 100000),  # noqa
                       remaining=random.randint(1000, 100000),  # noqa
                       estimated=random.randint(1000, 100000))  # noqa


def job():
    return Job(name="test_name", result="test_result",
               url="http://fake_url", report_url="http://fake_url",
               canceled=False, voting=False, retry=False,
               worker={"name": "fake_name"},
               time_tracker=time_tracker())


def buildset():
    return Buildset(name="test_name", buildset_id="12345,6", jobs=[],
                    enqueue_time=random.randint(1000, 100000),  # noqa
                    owner={'name': 'John smith'}, ref='12345',
                    review_url="http://fake_url")


class UserFactory:
    ROLE_ADMIN = 'admin'
    ROLE_USER = 'user'

    @staticmethod
    def get_user(role):
        if role == UserFactory.ROLE_ADMIN:
            attrs = {'full_name': 'Admin Admin',
                     'email': 'admin@acid.test'}
        else:
            attrs = {'full_name': 'Noname Guest',
                     'email': 'noname@guest.test'}
        return User(**attrs)


def status_request(filename=None, status_code=200):
    result = MagicMock()
    result.status_code = status_code
    filename = filename or config['zuul']['status_endpoint']
    with open(filename) as json_data:
        result.json = MagicMock(return_value=json.load(json_data))
    return MagicMock(return_value=result)


def load_status_data(name):
    with open(f'tests/static/{name}.json', "r") as data:
        return json.load(data)
