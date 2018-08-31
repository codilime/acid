# -*- coding: utf-8 -*-
from datetime import datetime

import pytest

from pony.orm import commit, db_session

from ..model import ZuulBuild, ZuulBuildSet


@pytest.fixture
def zuul_builds(mocker):
    mocker.patch('pony.orm.core.commit')

    return [make_build(build_number=104, buildset_id=5010),
            make_build(build_number=104, buildset_id=5010)]


@pytest.fixture
def zuul_build(mocker):
    mocker.patch('pony.orm.core.commit')

    def _make_build(build_number=104, buildset_id=5010, start_time=0,
                    end_time=0):
        if (start_time == 0):
            start_time = datetime(2018, 2, 23, 22, 0, 0)
        if (end_time == 0):
            end_time = datetime(2018, 2, 23, 23, 55, 0)
        build = make_build(build_number=build_number,
                           buildset_id=buildset_id,
                           start_time=start_time,
                           end_time=end_time)
        return build

    return _make_build


@pytest.fixture
def make_buildset():
    def _make_buildset(build_number=104, branch='master', number_of_builds=2):
        buildset = ZuulBuildSet(zuul_ref='Zef2180cdc7ff440daefe48d85ed91b48',
                                pipeline='periodic-nightly',
                                project='acid-test-dev',
                                change=None, patchset=None,
                                ref=f'refs/heads/{branch}',
                                message='Build succeeded.',
                                tenant='acid',
                                result='SUCCESS',
                                ref_url='http://acid.test/gitweb/',
                                oldrev='', newrev='')
        commit()
        for _ in range(number_of_builds):
            make_build(build_number=build_number, buildset_id=buildset.id)
        return buildset

    return _make_buildset


@db_session
def make_build(build_number, buildset_id, start_time=0, end_time=0):
    if (start_time == 0):
        start_time = datetime(2018, 2, 23, 22, 0, 0)
    if (end_time == 0):
        end_time = datetime(2018, 2, 23, 23, 55, 0)
    return ZuulBuild(buildset_id=buildset_id,
                     uuid='86394a77c99f45aba0e299b660214a9c',
                     job_name='acid-build-nightly',
                     result='SUCCESS',
                     start_time=start_time,
                     end_time=end_time,
                     voting=True,
                     log_url=f'http://logs.acid.test/{build_number}/865548a7/',
                     node_name='first_node')


@pytest.fixture
def populate_database():
    def _populate_database(count=10, branch='master', start_build_number=105):
        return [make_buildset()(build_number=str(start_build_number + x),
                                branch=branch)
                for x in range(count)]

    return _populate_database
