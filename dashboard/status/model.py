# -*- coding: utf-8 -*-
from time import time
from collections import namedtuple

from dashboard.config import config
from dashboard.status.time_utils import (epoch_to_datetime,
                                         milliseconds_to_seconds,
                                         seconds_to_time)


PipelineStat = namedtuple("PipelineStat", ["name", "buildsets_count"])


class Queue:
    def __init__(self, name, buildsets):
        self.name = name
        self.buildsets = buildsets

    def __len__(self):
        return len(self.buildsets)

    @classmethod
    def create(cls, queue):
        buildsets = []
        if len(queue['heads']) > 0:
            buildsets = [Buildset.create(b) for b in queue['heads'][0]]
        return cls(queue['name'], buildsets)


class Buildset:
    def __init__(self, name, buildset_id, jobs, enqueue_time, owner, ref,
                 review_url):
        self.name = name
        self.buildset_id = buildset_id
        self.jobs = jobs
        self.enqueue_time = milliseconds_to_seconds(enqueue_time)
        self.owner = owner
        self.ref = ref
        self.review_url = review_url

    def __len__(self):
        return len(self.jobs)

    @classmethod
    def create(cls, buildset):
        return cls(name=buildset['project'], buildset_id=buildset['id'],
                   jobs=[Job.create(j) for j in buildset['jobs']],
                   enqueue_time=buildset['enqueue_time'],
                   review_url=buildset['url'], owner=buildset['owner'],
                   ref=buildset['zuul_ref'])

    @property
    def elapsed_time(self):
        if self.enqueue_time:
            return seconds_to_time(
                time() - self.enqueue_time)
        return 0

    @property
    def remaining_time(self):
        try:
            remaining = max(j.time_tracker.remaining for j in self.jobs if
                            j.time_tracker.remaining is not None)
            return seconds_to_time(milliseconds_to_seconds(remaining))
        except ValueError:
            return None

    @property
    def start_datetime(self):
        try:
            start_time = min(j.time_tracker.start for j in self.jobs if
                             j.time_tracker.start is not None)
            return epoch_to_datetime(start_time)
        except ValueError:
            return None

    @property
    def status(self):
        if len(self.jobs) == 0:
            return 'Enqueued'

        for job in self.jobs:
            if job.result in Job.FAILING_RESULTS and job.voting:
                return 'Failing'
        return 'Succeeding'

    @property
    def progress(self):
        prog = 100
        if len(self.jobs) > 0:
            prog /= len(self.jobs)
        return prog

    @property
    def enqueue(self):
        if self.enqueue_time is not None:
            return epoch_to_datetime(self.enqueue_time)
        return None


class Job:
    FAILING_RESULTS = ('FAILURE', 'POST_FAILURE', 'RETRY_LIMIT', 'ERROR')

    def __init__(self, name, time_tracker, result, url, report_url, canceled,
                 voting, retry, worker):
        self.name = name
        self.time_tracker = time_tracker
        self.result = result
        self.url = url
        self.report_url = report_url
        self.canceled = canceled
        self.voting = voting
        self.retry = retry
        self.worker = worker

    @classmethod
    def create(cls, job):
        return cls(name=job['name'], result=job['result'], url=job['url'],
                   report_url=job['report_url'], canceled=job['canceled'],
                   voting=job['voting'], retry=job['retry'],
                   worker=job['worker'],
                   time_tracker=TimeTracker(job['start_time'],
                                            job['elapsed_time'],
                                            job['remaining_time'],
                                            job['estimated_time']))

    @property
    def progress(self):
        if int(self.time_tracker.estimated) <= 0 or \
            self.time_tracker.remaining is None:
            return 0
        else:
            return 100 - (float(self.time_tracker.remaining) / (
                float(self.time_tracker.estimated) * 10))

    @property
    def log_url(self):
        if self.result:
            return self.report_url
        return f'{config["zuul"]["url"].rstrip("/")}/{self.url}'


class TimeTracker:
    def __init__(self, start, elapsed, remaining, estimated):
        self.start = start
        self.elapsed = elapsed
        self.remaining = remaining
        self.estimated = estimated

    @property
    def start_to_datetime(self):
        if self.start is not None:
            return epoch_to_datetime(self.start)
        return None

    @property
    def elapsed_to_time(self):
        if self.elapsed:
            return seconds_to_time(milliseconds_to_seconds(self.elapsed))
        return None

    @property
    def remaining_to_time(self):
        if self.remaining is not None:
            return seconds_to_time(milliseconds_to_seconds(self.remaining))
        return None
