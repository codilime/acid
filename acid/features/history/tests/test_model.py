# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from pony.orm import db_session

import pytest

from acid.tests import DatabaseTestCase

from ..exceptions import PageOutOfRange
from ..service import BuildSetsPaginated
from ..model import ZuulBuildSet


@db_session
@pytest.mark.unit
class TestZuulBuildSet(DatabaseTestCase):
    # (kam193) TODO: randomize times
    def test_start_datetime_should_return_lowest_time(self, make_buildset):
        buildset = make_buildset(build_number=104)
        for index, build in enumerate(buildset.builds):
            build.start_time = datetime(2016 + index, 1, 1, 1, 1, 1)
        expected = datetime(2016, 1, 1, 1, 1, 1)
        assert buildset.start_datetime == expected

    def test_end_datetime_should_return_highest_time(self, make_buildset):
        buildset = make_buildset(build_number=104)
        for index, build in enumerate(buildset.builds):
            build.end_time = datetime(2016 + index, 1, 1, 1, 1, 1)
        expected = datetime(2016 + len(buildset.builds) - 1, 1, 1, 1, 1, 1)
        assert buildset.end_datetime == expected

    def test_branch_should_return_branch_name(self, make_buildset):
        buildset = make_buildset(branch='master')
        assert buildset.branch == 'master'

    def test_duration_should_return_timedelta(self, make_buildset):
        buildset = make_buildset()
        expected = timedelta(0, 6900)
        assert buildset.duration == expected

    def test_duration_wo_start_should_return_null(self, make_buildset, mocker):
        start = mocker.patch.object(ZuulBuildSet, 'start_datetime')
        start.__get__ = mocker.Mock(return_value=None)
        buildset = make_buildset()
        assert buildset.duration is None

    def test_duration_wo_end_should_return_null(self, make_buildset, mocker):
        end = mocker.patch.object(ZuulBuildSet, 'end_datetime')
        end.__get__ = mocker.Mock(return_value=None)
        buildset = make_buildset()
        assert buildset.duration is None

    def test_build_number_should_return_int(self, make_buildset):
        buildset = make_buildset(build_number=104)
        assert buildset.build_number == 104


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
