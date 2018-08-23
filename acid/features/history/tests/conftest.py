# -*- coding: utf-8 -*-
from datetime import datetime

import pytest

from pony.orm import commit, db_session

from ..model import ZuulBuild, ZuulBuildSet


@pytest.fixture
def zuul_build_set(mocker):
    return make_buildset(build_number=104)


@pytest.fixture
def zuul_builds(mocker):
    mocker.patch('pony.orm.core.commit')
    return [make_build(104, 5010), make_build(104, 5010)]


@db_session
def make_buildset(build_number, branch='master'):
    buildset = ZuulBuildSet(zuul_ref='Zef2180cdc7ff440daefe48d85ed91b48',
                            pipeline='periodic-nightly',
                            project='acid-test-dev',
                            change=None, patchset=None,
                            ref='refs/heads/master',
                            message='Build succeeded.',
                            tenant='acid',
                            result='SUCCESS',
                            ref_url='http://acid.test/gitweb/',
                            oldrev='', newrev='')
    commit()
    make_build(build_number, buildset.id)
    make_build(build_number, buildset.id)
    return buildset


@db_session
def make_build(build_number, buildset_id):
    return ZuulBuild(buildset_id=buildset_id,
                     uuid='86394a77c99f45aba0e299b660214a9c',
                     job_name='acid-build-nightly',
                     result='SUCCESS',
                     start_time=datetime(2018, 2, 23, 22, 0, 0),
                     end_time=datetime(2018, 2, 23, 23, 55, 0),
                     voting=True,
                     log_url=f'http://logs.acid.test/{build_number}/865548a7/',
                     node_name='first_node')


@pytest.fixture
def populate_database():
    def _populate_database(count=10, branch='master', start_build_number=105):
        return [make_buildset(branch, start_build_number + x)
                for x in range(count)]
    return _populate_database
