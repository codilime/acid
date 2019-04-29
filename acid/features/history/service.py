# -*- coding: utf-8 -*-
import logging
from collections import namedtuple

from pony.orm.serialization import to_json

from .exceptions import PageOutOfRange
from .model import ZuulBuildSet

Paginator = namedtuple("Paginator", ["pages", "previous_page",
                                     "next_page", "current_page"])
logger = logging.getLogger(__name__)


def pagination(number_of_buildsets, page, per_page, page_links):
    if number_of_buildsets < 0 or page < 1 or per_page < 1 or page_links < 0:
        raise ValueError

    number_of_pages = int((number_of_buildsets + per_page - 1) / per_page)

    if number_of_pages < 1:
        return Paginator(pages=[], previous_page=None,
                         next_page=None, current_page=page)

    previous_page = None if page == 1 else page - 1
    next_page = None if page == number_of_pages else page + 1

    pages = [p for p in range(page - page_links, page + page_links + 1)
             if 0 < p <= number_of_pages]

    if pages[0] != 1:
        pages = [1, None] + pages

    if pages[-1] != number_of_pages:
        pages.extend([None, number_of_pages])

    return Paginator(pages, previous_page, next_page, page)


class BuildSetsPaginated:
    def __init__(self, pipeline, max_latest_ref_count, per_page, refs,
                 build):
        self.pipeline = pipeline
        self.per_page = per_page
        self.max_latest_ref_count = max_latest_ref_count
        self.refs = refs
        self.build = build
        self.query = self._create_query()

    def __len__(self):
        return len(self.query)

    @property
    def all_refs(self):
        branches = ZuulBuildSet.get_refs_for_pipeline(self.pipeline)
        return branches

    @property
    def latest_refs(self):
        branches = ZuulBuildSet.get_refs_for_pipeline(
            self.pipeline, self.max_latest_ref_count)
        return branches

    def _is_page_in_range(self, page):
        return page > 0 and (page - 1) * self.per_page <= len(self)

    def _create_query(self):
        return ZuulBuildSet.get_buildsets(self.pipeline, self.refs, self.build)

    def fetch_page(self, page):
        if not self._is_page_in_range(page):
            raise PageOutOfRange
        self.page = self.query.page(page, self.per_page)

    def to_json(self, limit=0):
        try:
            limit = int(limit)
        except (TypeError, ValueError) as e:
            logger.warning(f'Invalid limit value, falling back to 0, {e}')
            limit = 0
        query = self.query
        if limit and limit > 0:
            query = query.limit(limit)
        result = to_json(bs for bs in query)
        return result
