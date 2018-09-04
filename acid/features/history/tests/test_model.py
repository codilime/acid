# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from pony.orm import db_session

import pytest

from acid.tests import DatabaseTestCase

from ..exceptions import PageOutOfRange
from ..service import BuildSetsPaginated
from ..model import ZuulBuildSet


@pytest.mark.unit
class TestZuulBuildSet(DatabaseTestCase):
    @db_session
    def test_start_datetime_should_return_lowest_time(self, make_buildset):
        buildset = make_buildset()
        expected = datetime(2018, 2, 23, 22, 0, 0)
        assert buildset.start_datetime == expected

    @pytest.mark.parametrize("start_time, end_time ,expected", [
        ('2018-02-23 22:00:00', None, None),
        (None, '2018-02-23 23:55:00', None),
        (None, None, None)
    ])
    @db_session
    def test_start_datetime_return_none(self, make_buildset,
                                        start_time, end_time, expected):
        buildset = make_buildset(start_time=start_time, end_time=end_time)
        assert buildset.start_datetime is expected

    @db_session
    def test_end_datetime_should_return_highest_time(self, make_buildset):
        buildset = make_buildset()
        expected = datetime(2018, 2, 23, 23, 55, 0)
        print(buildset.end_datetime)
        assert buildset.end_datetime == expected

    @pytest.mark.parametrize("start_time, end_time ,expected", [
        ('2018-02-23 22:00:00', None, None),
        (None, '2018-02-23 23:55:00', None),
        (None, None, None)
    ])
    @db_session
    def test_end_datetime_return_none(self, make_buildset, start_time, end_time,
                                      expected):
        buildset = make_buildset(start_time=start_time, end_time=end_time)
        assert buildset.end_datetime is expected

    @db_session
    def test_branch_should_return_branch_name(self, make_buildset):
        buildset = make_buildset(branch='master')
        assert buildset.branch == 'master'

    @db_session
    def test_duration_should_return_timedelta(self, make_buildset):
        buildset = make_buildset()
        expected = timedelta(0, 6900)
        assert buildset.duration == expected

    @db_session
    def test_duration_wo_start_should_return_null(self, make_buildset, mocker):
        start = mocker.patch.object(ZuulBuildSet, 'start_datetime')
        start.__get__ = mocker.Mock(return_value=None)
        buildset = make_buildset()
        assert buildset.duration is None

    @db_session
    def test_duration_wo_end_should_return_null(self, make_buildset, mocker):
        end = mocker.patch.object(ZuulBuildSet, 'end_datetime')
        end.__get__ = mocker.Mock(return_value=None)
        buildset = make_buildset()
        assert buildset.duration is None

    @db_session
    def test_build_number_should_return_int(self, make_buildset):
        buildset = make_buildset(build_number=104)
        assert buildset.build_number == 104

    @db_session
    def test_build_number_return_none_if_no_build_number(self, make_buildset):
        buildset = make_buildset(build_number=None)
        assert buildset.build_number is None

    @db_session
    def test_get_branches_return_branches(self, make_buildset):
        make_buildset(branch='master')
        make_buildset(branch='gimp')
        branches = list(ZuulBuildSet.get_branches())
        expected = ['master', 'gimp']
        assert branches == expected

    @db_session
    def test_get_for_pipeline_return_pipelines(self,
                                               database_with_buildsets):
        database = database_with_buildsets(count=2)
        database[0].pipeline = "one"
        return_buildsets = list(ZuulBuildSet.get_for_pipeline(pipeline='one'))
        expected = [database[0]]
        assert return_buildsets == expected

    @db_session
    def test_get_filtered_if_branch_is_not_in_branches(self,
                                                       database_with_buildsets):
        database = database_with_buildsets()
        for buildset in database:
            buildset.ref = 'refs/heads/gimp'
        filtered_buildsets = list(ZuulBuildSet.get_filtered(
            pipeline='periodic-nightly',
            branch='master',
            build='105'))
        expected = [database[0]]
        assert filtered_buildsets == expected

    @db_session
    def test_get_filtered_if_build_is_none(self,
                                           database_with_buildsets):
        buildsets = database_with_buildsets()
        filtered_buildsets = list(ZuulBuildSet.get_filtered(
            pipeline='periodic-nightly',
            branch='master',
            build=None))
        expected = buildsets[::-1]
        assert filtered_buildsets == expected

    @db_session
    def test_duration_return_value(self, make_buildset):
        buildset = make_buildset(number_of_builds=1,
                                 start_time='2018-02-23 22:00:00',
                                 end_time='2018-02-23 23:55:00')
        builds_duration = list(buildset.builds)[0].duration
        expected = timedelta(0, 6900)
        assert builds_duration == expected

    @pytest.mark.parametrize("start_time, end_time ,expected", [
        ('2018-02-23 22:00:00', None, None),
        (None, '2018-02-23 23:55:00', None),
        (None, None, None)
    ])
    @db_session
    def test_duration_return_none(self, make_buildset, start_time, end_time,
                                  expected):
        buildset = make_buildset(number_of_builds=1, start_time=start_time,
                                 end_time=end_time)
        builds_duration = list(buildset.builds)[0].duration
        assert builds_duration == expected


@pytest.mark.unit
class TestBuildSetPaginated:
    def test_create_buildsets_history_object(self, mocker):
        mocker.patch.object(ZuulBuildSet, 'get_for_pipeline')
        buildsets = BuildSetsPaginated(pipeline="foo", per_page=20)
        assert buildsets.per_page == 20

    def test_create_query(self, mocker):
        get_for_pipeline = mocker.patch.object(ZuulBuildSet, 'get_for_pipeline')
        BuildSetsPaginated(pipeline="foo", per_page=20)
        get_for_pipeline.assert_called_with("foo")

    def test_fetch_raises_when_page_is_out_of_range(self, mocker):
        get_for_pipeline = mocker.patch.object(ZuulBuildSet, 'get_for_pipeline')
        get_for_pipeline.return_value = [
            'first_element', 'second_element', 'third_element']

        buildsets = BuildSetsPaginated(pipeline="foo", per_page=20)

        with pytest.raises(PageOutOfRange):
            buildsets.fetch_page(2)

    def test_fetch_set_correct_page(self, mocker):
        get_for_pipeline = mocker.patch.object(ZuulBuildSet, 'get_for_pipeline')
        data = ['first_element', 'second_element', 'third_element']

        query = mocker.MagicMock()
        query.__len__ = lambda x: len(data)
        query.page = mocker.MagicMock()
        query.page.return_value = data
        get_for_pipeline.return_value = query

        buildset = BuildSetsPaginated(pipeline="foo", per_page=20)
        buildset.fetch_page(page=1)

        assert buildset.page == data
        query.page.assert_called_with(1, 20)
