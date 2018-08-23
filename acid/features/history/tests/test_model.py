# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

import pytest

from acid.tests import DatabaseTestCase

from ..exceptions import PageOutOfRange
from ..service import BuildSetsPaginated
from ..model import ZuulBuildSet


@pytest.mark.unit
class TestZuulBuildSet(DatabaseTestCase):
    # (kam193) TODO: randomize times
    def test_start_datetime_should_return_lowest_time(self, zuul_build_set):
        expected = datetime(2018, 2, 23, 22, 0, 0)
        assert zuul_build_set.start_datetime == expected

    def test_end_datetime_should_return_highest_time(self, zuul_build_set):
        expected = datetime(2018, 2, 23, 23, 55, 0)
        assert zuul_build_set.end_datetime == expected

    def test_branch_should_return_branch_name(self, zuul_build_set):
        assert zuul_build_set.branch == 'master'

    def test_duration_should_return_timedelta(self, zuul_build_set):
        expected = timedelta(0, 6900)
        assert zuul_build_set.duration == expected

    def test_duration_wo_start_should_return_null(self, zuul_build_set, mocker):
        start = mocker.patch.object(ZuulBuildSet, 'start_datetime')
        start.__get__ = mocker.Mock(return_value=None)
        assert zuul_build_set.duration is None

    def test_duration_wo_end_should_return_null(self, zuul_build_set, mocker):
        end = mocker.patch.object(ZuulBuildSet, 'end_datetime')
        end.__get__ = mocker.Mock(return_value=None)
        assert zuul_build_set.duration is None

    def test_build_number_should_return_int(self, zuul_build_set):
        expected = 104
        assert zuul_build_set.build_number == expected


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
