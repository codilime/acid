# -*- coding: utf-8 -*-
import pytest

from ..service import Paginator, pagination


@pytest.mark.unit
class TestPagination:
    def test_zero_buildsets_should_return_empty_paginator(self):
        paginator = pagination(number_of_buildsets=0,
                               page=1,
                               per_page=10,
                               page_links=5)

        expected = Paginator(pages=[],
                             previous_page=None,
                             next_page=None,
                             current_page=1)
        assert paginator == expected

    def test_current_page_first_should_return_no_previous_page(self):
        paginator = pagination(number_of_buildsets=100,
                               page=1,
                               per_page=20,
                               page_links=4)

        expected = Paginator(pages=[1, 2, 3, 4, 5],
                             previous_page=None,
                             next_page=2,
                             current_page=1)
        assert paginator == expected

    def test_current_page_last_should_return_no_next_page(self):
        paginator = pagination(number_of_buildsets=100,
                               page=5,
                               per_page=20,
                               page_links=4)

        expected = Paginator(pages=[1, 2, 3, 4, 5],
                             previous_page=4,
                             next_page=None,
                             current_page=5)
        assert paginator == expected

    def test_200_buildsets_20_per_page_should_return_10_pages(self):
        paginator = pagination(number_of_buildsets=200,
                               page=1,
                               per_page=20,
                               page_links=20)

        expected = Paginator(pages=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                             previous_page=None,
                             next_page=2,
                             current_page=1)
        assert paginator == expected

    def test_201_buildsets_20_per_page_should_return_11_pages(self):
        paginator = pagination(number_of_buildsets=201,
                               page=1,
                               per_page=20,
                               page_links=20)

        expected = Paginator(pages=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
                             previous_page=None,
                             next_page=2,
                             current_page=1)
        assert paginator == expected

    def test_40_buildsets_10_per_page_should_return_4_pages(self):
        paginator = pagination(number_of_buildsets=40,
                               page=1,
                               per_page=10,
                               page_links=10)

        expected = Paginator(pages=[1, 2, 3, 4],
                             previous_page=None,
                             next_page=2,
                             current_page=1)
        assert paginator == expected

    def test_45_buildsets_10_per_page_should_return_5_pages(self):
        paginator = pagination(number_of_buildsets=45,
                               page=1,
                               per_page=10,
                               page_links=10)

        expected = Paginator(pages=[1, 2, 3, 4, 5],
                             previous_page=None,
                             next_page=2,
                             current_page=1)
        assert paginator == expected

    def test_current_page_5_of_10_should_return_previous_and_next_page(self):
        paginator = pagination(number_of_buildsets=100,
                               page=5,
                               per_page=10,
                               page_links=5)

        expected = Paginator(pages=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                             previous_page=4,
                             next_page=6,
                             current_page=5)
        assert paginator == expected

    def test_5_page_links_on_page_10_should_return_5_prev_and_next_pages(self):
        paginator = pagination(number_of_buildsets=400,
                               page=10,
                               per_page=20,
                               page_links=5)

        expected = Paginator(pages=[1, None, 5, 6, 7, 8, 9, 10, 11, 12,
                                    13, 14, 15, None, 20],
                             previous_page=9,
                             next_page=11,
                             current_page=10)
        assert paginator == expected

    def test_3_pages_links_on_page_5_should_return_3_prev_and_next_pages(self):
        paginator = pagination(number_of_buildsets=400,
                               page=5,
                               per_page=20,
                               page_links=3)

        expected = Paginator(pages=[1, None, 2, 3, 4, 5, 6, 7, 8, None, 20],
                             previous_page=4,
                             next_page=6,
                             current_page=5)
        assert paginator == expected

    @pytest.mark.parametrize("value,exc", [(0, ValueError),
                                           (-5, ValueError),
                                           (None, TypeError)])
    def test_per_page_incorrect_value_should_raise_exc(self, value, exc):
        with pytest.raises(exc):
            pagination(number_of_buildsets=200,
                       page=1,
                       per_page=value,
                       page_links=5)

    @pytest.mark.parametrize("value,exc", [(0, ValueError),
                                           (-5, ValueError),
                                           (None, TypeError)])
    def test_current_page_incorrect_value_should_raise_exc(self, value, exc):
        with pytest.raises(exc):
            pagination(number_of_buildsets=200,
                       page=value,
                       per_page=20,
                       page_links=5)

    @pytest.mark.parametrize("value,exc", [(-1, ValueError),
                                           (None, TypeError)])
    def test_buildsets_incorrect_value_should_raise_exc(self, value, exc):
        with pytest.raises(exc):
            pagination(number_of_buildsets=value,
                       page=1,
                       per_page=20,
                       page_links=5)

    @pytest.mark.parametrize("value,exc", [(-1, ValueError),
                                           (None, TypeError)])
    def test_page_links_incorrect_value_should_raise_exc(self, value, exc):
        with pytest.raises(exc):
            pagination(number_of_buildsets=200,
                       page=1,
                       per_page=20,
                       page_links=value)
