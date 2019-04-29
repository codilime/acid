# -*- coding: utf-8 -*-
from datetime import datetime

from pony.orm import Optional, Set, desc, select

from acid.db import db


class ZuulBuildSet(db.Entity):
    _table_ = "zuul_buildset"
    zuul_ref = Optional(str)
    pipeline = Optional(str)
    project = Optional(str)
    change = Optional(int)
    patchset = Optional(int)
    ref = Optional(str)
    message = Optional(str)
    tenant = Optional(str)
    result = Optional(str)
    ref_url = Optional(str)
    oldrev = Optional(str)
    newrev = Optional(str)
    builds = Set("ZuulBuild")

    @property
    def start_datetime(self):
        try:
            return min(b.start_time for b in self.builds if
                       b.start_time and b.end_time)
        except ValueError:
            return None

    @property
    def end_datetime(self):
        try:
            return max(b.end_time for b in self.builds if
                       b.start_time and b.end_time is not None)
        except ValueError:
            return None

    @property
    def branch(self):
        return '/'.join(self.ref.split('/')[2:])

    @property
    def duration(self):
        start = self.start_datetime
        end = self.end_datetime

        if start and end:
            return end - start
        return None

    @property
    def build_number(self):
        for b in self.builds:
            if b.build_number is not None:
                return b.build_number
        return None

    @classmethod
    def get_refs_for_pipeline(cls, pipeline, max_ref_count=None):
        query = select(b for b in cls if b.pipeline == pipeline)
        query = query.order_by(desc(cls.id))
        if max_ref_count is not None:
            query = query.limit(max_ref_count)
        return {b.ref for b in query}

    @classmethod
    def get_buildsets(cls, pipeline=None, refs=None, build=None):
        query = select(
            bs for bs in cls
            if len(bs.builds) > 0).sort_by(desc(cls.id))
        if pipeline:
            query = query.where(lambda bs: bs.pipeline == pipeline)
        if refs and len(refs) > 0:
            query = query.where(lambda bs: bs.ref in refs)
        if build and build.isnumeric():
            build_str = f'/{build}/'
            query = query.where(
                lambda bs:
                len(
                    select(b for b in bs.builds if build_str in b.log_url)
                ) > 0)
        return query


class ZuulBuild(db.Entity):
    _table_ = "zuul_build"
    buildset_id = Optional(ZuulBuildSet)
    uuid = Optional(str)
    job_name = Optional(str)
    result = Optional(str)
    start_time = Optional(datetime, 6)
    end_time = Optional(datetime, 6)
    voting = Optional(bool)
    log_url = Optional(str)
    node_name = Optional(str)

    @property
    def build_number(self):
        return self._get_build_number_from_log_url()

    @property
    def duration(self):
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return None

    def _get_build_number_from_log_url(self):
        try:
            split_url = self.log_url.split('/')
            # there is another log_url format (on logs.contrail.juniper.net)
            # where element [-3] is never a int, but instead [-4] is
            if split_url[-3].isdigit():
                return int(split_url[-3])
            else:
                return int(split_url[-4])
        except (ValueError, IndexError):
            return None
