# -*- coding: utf-8 -*-
import datetime

import pytest

from pony.orm import commit, db_session

from ..model import ZuulBuild, ZuulBuildSet

TIME_START = '2018-02-23 22:00:00'
TIME_END = '2018-02-23 23:55:00'


def _datetime_to_seconds(t_stamp):
    return int(t_stamp.strftime("%s")) if t_stamp else None


def _seconds_to_datetime(t_epoch):
    return datetime.datetime.fromtimestamp(t_epoch).strftime(
        '%Y-%m-%d %H:%M:%S') if t_epoch else None


def _convert_to_timestamp(timestamp):
    if isinstance(timestamp, datetime.datetime):
        return timestamp
    else:
        try:
            return datetime.datetime.strptime(
                timestamp, '%Y-%m-%d %H:%M:%S')
        except (TypeError, ValueError):
            return None


def _seconds_table_between_range(start_sec, end_sec, n):
    if n < 2:
        return [start_sec]

    if start_sec and end_sec:
        # calculating step value to generate n-1 elements. We gonna
        # add end_time in the end, that's why n-1. This is math thats
        # calculate needed step for range to get n-1 elements.
        step = 2 * (n - 1) + 1
        epoch_delta = int((end_sec - start_sec) / step)
        epoch_list = [e for e in
                      range(start_sec, end_sec, epoch_delta)]
        # drop last elements if range return even number of elements
        # we need odd elements
        if end_sec - epoch_list[-1] < epoch_delta:
            epoch_list = epoch_list[:-1]
        return sorted(epoch_list)
    else:
        return [None] * (2 * (n - 1) + 1)


def _return_starting_and_ending_times(start_time, end_time, no_of_builds):
    if no_of_builds < 1:
        return [], []

    start_time, end_time = map(_convert_to_timestamp, (start_time, end_time))
    start_time, end_time = map(_datetime_to_seconds, (start_time, end_time))

    all_epoch_times = _seconds_table_between_range(start_time, end_time,
                                                   no_of_builds)
    all_epoch_times = all_epoch_times + [end_time]
    all_epoch_times = list(map(_seconds_to_datetime, all_epoch_times))

    starting_times = all_epoch_times[:no_of_builds]
    ending_times = all_epoch_times[no_of_builds:]

    return starting_times, ending_times


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

        start_times, end_times = _return_starting_and_ending_times(
            start_time=start_time, end_time=end_time,
            no_of_builds=number_of_builds)

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
