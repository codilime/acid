# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

import pytest

from pony.orm import commit, db_session

from ..model import ZuulBuild, ZuulBuildSet

TIME_START = '2018-02-23 22:00:00'
TIME_END = '2018-02-23 23:55:00'

@db_session
def make_build(start_time, end_time, build_number=104, buildset_id=5010):

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
def make_buildset():

    def return_starting_and_ending_times(start_time, end_time, builds_number):
        try:
            start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
        except:
            start_time = None
        try:
            end_time = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
        except:
            end_time = None

        if (start_time and end_time):
            time_diff = (end_time - start_time).total_seconds()
        else:
            time_diff = 0

        starting_times = [start_time]
        ending_times = [end_time]

        if builds_number > 1:
            time_step = (time_diff / 2) / builds_number
            for each in range(1, builds_number):
                if start_time:
                    start = start_time + each * timedelta(seconds=time_step)
                else:
                    start = None
                starting_times.append(start)
                if end_time:
                    end = end_time - each * timedelta(seconds=time_step)
                else:
                    end = None
                ending_times.append(end)

        return starting_times, ending_times

    def _make_buildset(build_number=104, branch='master', number_of_builds=5,
                       start_time=TIME_START, end_time=TIME_END):
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

        start_times, end_times = return_starting_and_ending_times(
            start_time=start_time, end_time=end_time,
            builds_number=number_of_builds)

        for index in range(number_of_builds):
            make_build(build_number=build_number, buildset_id=buildset.id,
                       start_time=start_times[index],
                       end_time=end_times[index])
        return buildset

    return _make_buildset


@pytest.fixture
def database_with_buildsets():
    def _create_database_with_buildsets(count=10, branch='master',
                                        start_build_number=105):
        return [make_buildset()(build_number=str(start_build_number + x),
                                branch=branch)
                for x in range(count)]

    return _create_database_with_buildsets
