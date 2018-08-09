# -*- coding: utf-8 -*-
import unittest
from unittest.mock import MagicMock, patch

from ..exceptions import PageOutOfRange
from ..service import BuildSetsPaginated
from ..model import ZuulBuildSet


class TestBuildSets(unittest.TestCase):
    @patch.object(ZuulBuildSet, 'get_for_pipeline')
    def test_create_buildsets_history_object(self, get_for_pipeline):
        buildsets = BuildSetsPaginated(pipeline="foo", per_page=20)

        self.assertEqual(buildsets.per_page, 20)

    @patch.object(ZuulBuildSet, 'get_for_pipeline')
    def test_create_query(self, get_for_pipeline):
        BuildSetsPaginated(pipeline="foo", per_page=20)

        get_for_pipeline.assert_called_with("foo")

    @patch.object(ZuulBuildSet, 'get_for_pipeline')
    def test_fetch_raises_when_page_is_out_of_range(self, get_for_pipeline):
        get_for_pipeline.return_value = [
            'first_element', 'second_element', 'third_element']

        buildsets = BuildSetsPaginated(pipeline="foo", per_page=20)

        with self.assertRaises(PageOutOfRange):
            buildsets.fetch_page(2)

    @patch.object(ZuulBuildSet, 'get_for_pipeline')
    def test_fetch_set_correct_page(self, get_for_pipeline):
        data = ['first_element', 'second_element', 'third_element']

        query = self._query_mock(data)
        get_for_pipeline.return_value = query

        buildset = BuildSetsPaginated(pipeline="foo", per_page=20)
        buildset.fetch_page(page=1)

        self.assertEqual(buildset.page, data)
        query.page.assert_called_with(1, 20)

    @staticmethod
    def _query_mock(data):
        query = MagicMock()
        query.__len__ = lambda x: len(data)
        query.page = MagicMock()
        query.page.return_value = data
        return query