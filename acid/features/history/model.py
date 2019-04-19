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
    def get_branches(cls):
        branches = select(b.ref for b in cls)
        return branches

    @classmethod
    def get_for_pipeline(cls, pipeline):
        return select(
            bs for bs in cls
            if bs.pipeline == pipeline and
            len(select(b for b in bs.builds)) > 0).sort_by(desc(cls.id))

    @classmethod
    def get_filtered(cls, pipeline, branches, build=''):
        all_branches = list(cls.get_branches())
        branches = [x for x in branches if x in all_branches]
        if (len(branches) == 0):
            branches = all_branches

        if build is None or not build.isnumeric():
            build = ''
        else:
            build = f'/{build}/'

        return select(
            bs for bs in cls if
            bs.pipeline == pipeline and bs.ref in branches and
            len(select(b for b in bs.builds if
                       build in b.log_url)) > 0).sort_by(desc(cls.id))


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
