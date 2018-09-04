# -*- coding: utf-8 -*-
import time

import pytest

from pony.orm import commit, db_session

from ..model import ZuulBuild, ZuulBuildSet

import random

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



        # def validate_start_and_end_time(start, end):
        #     try:
        #         start_time = time.strptime(start, '%Y-%m-%d %H:%M:%S')
        #     except TypeError:
        #         start_time = None
        #     try:
        #         end_time = time.strptime(end, '%Y-%m-%d %H:%M:%S')
        #     except TypeError:
        #         end_time = None
        #
        #     return start_time, end_time
        #
        # def epoch_from_date(t_stamp):
        #     return int(time.mktime(t_stamp)) + 3600 if t_stamp else None
        #
        # def date_from_epoch(t_epoch):
        #     return time.strftime('%Y-%m-%d %H:%M:%S',
        #                          time.gmtime(t_epoch)) if t_epoch else None
        #
        # def return_random_epoch_times(start, end, n):
        #     def randoms_seconds(begin, end, n):
        #         if begin and end:
        #             delta = int((end - begin) / 2)
        #         else:
        #             delta = 3600
        #
        #         return random.sample(range(1, delta), n - 1)
        #
        #     def generate_random_times(random_table, start, end, n):
        #         if start:
        #             start_list = [start + random_second for
        #                           random_second in random_table]
        #             start_list = [start] + start_list
        #         else:
        #             start_list = [None] * n
        #
        #         if end:
        #             end_list = [end - random_second for
        #                         random_second in random_table]
        #             end_list = [end] + end_list
        #         else:
        #             end_list = [None] * n
        #
        #         return start_list, end_list
        #
        #     random_seconds = randoms_seconds(start, end, n)
        #     starting_times, ending_times = generate_random_times(random_seconds,
        #                                                          start, end, n)
        #
        #     return starting_times, ending_times
        #
        #
        #
        # start_time, end_time = validate_start_and_end_time(start_time, end_time)
        # start_time, end_time = map(epoch_from_date, (start_time, end_time))
        # starting_times, ending_times = return_random_epoch_times(start_time,
        #                                                          end_time,
        #                                                          builds_number)
        # starting_times = map(date_from_epoch, starting_times)
        # ending_times = map(date_from_epoch, ending_times)

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
