# -*- coding: utf-8 -*-
from datetime import datetime

import pytest

from pony.orm import db_session

from ..model import ZuulBuild, ZuulBuildSet


@db_session
@pytest.fixture
def zuul_build_set(mocker):
    return ZuulBuildSet(zuul_ref='Zef2180cdc7ff440daefe48d85ed91b48',
                        pipeline='periodic-nightly',
                        project='acid-test-dev',
                        change=None, patchset=None,
                        ref='refs/heads/master',
                        message='Build succeeded.',
                        tenant='acid',
                        result='SUCCESS',
                        ref_url='http://acid.test/gitweb/',
                        oldrev='', newrev='',
                        builds=zuul_builds(mocker))


@db_session
@pytest.fixture
def zuul_builds(mocker):
    mocker.patch('pony.orm.core.commit')
    return [ZuulBuild(buildset_id=5010,
                      uuid='86394a77c99f45aba0e299b660214a9c',
                      job_name='acid-build-nightly',
                      result='SUCCESS',
                      start_time=datetime(2018, 2, 23, 22, 18, 15),
                      end_time=datetime(2018, 2, 23, 23, 18, 46),
                      voting=True,
                      log_url='http://logs.acid.test/104/865548a7/',
                      node_name='first_node'),
            ZuulBuild(buildset_id=5010,
                      uuid='86394a77c99f45aba0e299b660214a9c',
                      job_name='acid-build-nightly',
                      result='SUCCESS',
                      start_time=datetime(2018, 2, 23, 22, 0, 0),
                      end_time=datetime(2018, 2, 23, 23, 55, 0),
                      voting=True,
                      log_url='http://logs.acid.test/104/865548a7/',
                      node_name='first_node')]
