# -*- coding: utf-8 -*-
import unittest
from unittest import mock

from . import fixtures

from acid.config import config

from ..model import Buildset, Job, TimeTracker
from ..time_utils import (epoch_to_datetime, milliseconds_to_seconds,
                          seconds_to_time)


class TestTimeTracker(unittest.TestCase):
    def test_none_start_to_datetime_should_return_none(self):
        tt = fixtures.time_tracker()
        tt.start = None
        result = tt.start_to_datetime
        self.assertIsNone(result)

    def test_none_elapsed_to_time_should_return_none(self):
        tt = fixtures.time_tracker()
        tt.elapsed = None
        result = tt.elapsed_to_time
        self.assertIsNone(result)

    def test_none_remaining_to_time_should_return_none(self):
        tt = fixtures.time_tracker()
        tt.remaining = None
        result = tt.remaining_to_time
        self.assertIsNone(result)

    def test_zero_remaining_to_time_should_return_zero(self):
        tt = fixtures.time_tracker()
        tt.remaining = 0
        result = tt.remaining_to_time
        expected = seconds_to_time(0)
        self.assertEqual(result, expected)

    def test_zero_start_to_datetime_should_return_data(self):
        tt = fixtures.time_tracker()
        result = tt.start_to_datetime
        expected = epoch_to_datetime(tt.start)
        self.assertEqual(result, expected)

    def test_hour_elapsed_to_time_should_return_data(self):
        tt = fixtures.time_tracker()
        result = tt.elapsed_to_time
        expected = seconds_to_time(milliseconds_to_seconds(tt.elapsed))
        self.assertEqual(result, expected)

    def test_hour_remaining_to_time_should_return_data(self):
        tt = fixtures.time_tracker()
        result = tt.remaining_to_time
        expected = seconds_to_time(milliseconds_to_seconds(tt.remaining))
        self.assertEqual(result, expected)


class TestJob(unittest.TestCase):
    def compare_jobs(self, job1, job2, msg=None):
        self.assertDictEqual(job1.time_tracker.__dict__,
                             job2.time_tracker.__dict__, msg=msg)

        job1.time_tracker = job2.time_tracker = None

        self.assertDictEqual(job1.__dict__, job2.__dict__, msg=msg)

    def test_create_should_return_expected_data(self):
        job_data = {"url": "http://fake_url",
                    "start_time": 1, "elapsed_time": 1,
                    "retry": False, "voting": False,
                    "report_url": "http://fake_url",
                    "worker": {"name": "fake_name"},
                    "remaining_time": 1, "canceled": False,
                    "estimated_time": 1,
                    "result": "test_result",
                    "name": "test_name"}

        expected_job = Job(name="test_name", result="test_result",
                           url="http://fake_url", report_url="http://fake_url",
                           canceled=False, voting=False, retry=False,
                           worker={"name": "fake_name"},
                           time_tracker=TimeTracker(start=1,
                                                    elapsed=1,
                                                    remaining=1,
                                                    estimated=1))

        return_job = Job.create(job=job_data)

        self.addTypeEqualityFunc(Job, self.compare_jobs)
        self.assertEquals(expected_job, return_job)

    def test_no_remaining_should_return_100(self):
        test_job = fixtures.job()
        test_job.time_tracker.remaining = 0
        expected = 100
        result = test_job.progress
        self.assertEqual(result, expected)

    def test_no_estimated_should_return_0(self):
        test_job = fixtures.job()
        test_job.time_tracker.estimated = 0
        expected = 0
        result = test_job.progress
        self.assertEqual(result, expected)

    def test_none_remaining_should_return_0(self):
        test_job = fixtures.job()
        test_job.time_tracker.remaining = None
        expected = 0
        result = test_job.progress
        self.assertEqual(result, expected)

    def test_valid_progress_should_return_data(self):
        test_job = fixtures.job()
        test_job.time_tracker.remaining = 1000
        test_job.time_tracker.estimated = 10
        expected = 90
        result = test_job.progress
        self.assertEqual(result, expected)

    def test_nonempty_result_should_return_data(self):
        test_job = fixtures.job()
        test_job.result = "test"
        test_job.report_url = "http://fake_url"
        expected = "http://fake_url"
        result = test_job.log_url
        self.assertEqual(result, expected)

    def test_empty_result_with_multiple_slashes_should_return_url(self):
        test_job = fixtures.job()
        test_job.result = None
        test_job.url = "fake_endpoint"
        expected = "http://fake_url/fake_endpoint"
        with mock.patch.dict(config['zuul'], {'url': 'http://fake_url/////'}):
            result = test_job.log_url
        self.assertEqual(result, expected)

    def test_empty_result_wo_slashes_should_return_url(self):
        test_job = fixtures.job()
        test_job.result = None
        test_job.url = "fake_endpoint"
        expected = "http://fake_url/fake_endpoint"
        with mock.patch.dict(config['zuul'], {'url': 'http://fake_url'}):
            result = test_job.log_url
        self.assertEqual(result, expected)


class TestBuildset(unittest.TestCase):
    def compare_buildsets(self, buildset1, buildset2, msg=None):
        # assumes buildset has empty job list
        self.assertDictEqual(buildset1.owner, buildset2.owner, msg=msg)

        buildset1.owner = buildset2.owner = None

        self.assertDictEqual(buildset1.__dict__, buildset2.__dict__, msg=msg)

    def test_create_should_return_expected_data(self):
        buildset_data = {"url": "http://fake_url",
                         "owner": {'name': 'John smith'}, "jobs": [],
                         "item_ahead": None, "live": True,
                         "remaining_time": 1812372, "failing_reasons": [],
                         "items_behind": [], "project": "test_name",
                         "id": "12345,6", "active": True, "zuul_ref": "12345",
                         "enqueue_time": 0}

        expected_buildset = fixtures.buildset()
        expected_buildset.enqueue_time = 0

        result_buildset = Buildset.create(buildset=buildset_data)

        self.addTypeEqualityFunc(Buildset, self.compare_buildsets)
        self.assertEquals(expected_buildset, result_buildset)

    def test_none_elapsed_time_should_return_0(self):
        test_buildset = fixtures.buildset()
        test_buildset.enqueue_time = None
        expected = 0
        result = test_buildset.elapsed_time
        self.assertEqual(result, expected)

    def test_zero_elapsed_time_should_return_0(self):
        test_buildset = fixtures.buildset()
        test_buildset.enqueue_time = 0
        expected = 0
        result = test_buildset.elapsed_time
        self.assertEqual(result, expected)

    @mock.patch('acid.features.status.model.time')
    def test_valid_elapsed_time_should_return_expected_time(self, time):
        test_buildset = fixtures.buildset()
        fixed_time = 1532004145.20974
        time.return_value = fixed_time
        result = test_buildset.elapsed_time
        expected = seconds_to_time(fixed_time - test_buildset.enqueue_time)
        self.assertEqual(result, expected)

    def test_remaining_wo_jobs_should_return_none(self):
        test_buildset = fixtures.buildset()
        test_buildset.jobs = []
        result = test_buildset.remaining_time
        self.assertIsNone(result)

    def test_remaining_with_job_wo_remaining_should_return_none(self):
        test_buildset = fixtures.buildset()
        test_job = fixtures.job()
        test_job.time_tracker.remaining = None
        test_buildset.jobs = [test_job]
        result = test_buildset.remaining_time
        self.assertIsNone(result)

    def test_remaining_with_multiple_jobs_should_return_longest_time(self):
        test_buildset = fixtures.buildset()
        test_jobs = [fixtures.job() for x in range(3)]
        max_time = max(job.time_tracker.remaining for job in test_jobs)
        test_buildset.jobs = test_jobs
        result = test_buildset.remaining_time
        expected = seconds_to_time(milliseconds_to_seconds(max_time))
        self.assertEqual(result, expected)

    def test_start_wo_jobs_should_return_none(self):
        test_buildset = fixtures.buildset()
        test_buildset.jobs = []
        result = test_buildset.start_datetime
        self.assertIsNone(result)

    def test_start_with_job_wo_start_should_return_none(self):
        test_buildset = fixtures.buildset()
        test_job = fixtures.job()
        test_job.time_tracker.start = None
        test_buildset.jobs = [test_job]
        result = test_buildset.start_datetime
        self.assertIsNone(result)

    def test_start_with_multiple_jobs_should_return_earliest_time(self):
        test_buildset = fixtures.buildset()
        test_jobs = [fixtures.job() for x in range(3)]
        min_time = min(job.time_tracker.start for job in test_jobs)
        test_buildset.jobs = test_jobs
        result = test_buildset.start_datetime
        expected = epoch_to_datetime(min_time)
        self.assertEqual(result, expected)

    def test_status_wo_jobs_should_have_enqueued_status(self):
        test_buildset = fixtures.buildset()
        test_buildset.jobs = []
        expected = 'Enqueued'
        result = test_buildset.status
        self.assertEqual(result, expected)

    def test_status_with_any_failing_voting_job_should_have_fail_status(self):
        test_buildset = fixtures.buildset()
        test_job = fixtures.job()
        test_job.voting = True
        test_buildset.jobs = [test_job]
        expected = "Failing"

        for fresult in Job.FAILING_RESULTS:
            test_job.result = fresult
            result = test_buildset.status
            self.assertEqual(result, expected)

    def test_status_with_failing_non_voting_job_should_have_success_status(self):
        test_buildset = fixtures.buildset()
        test_jobs = [fixtures.job() for _ in Job.FAILING_RESULTS]
        for job, job_result in zip(test_jobs, Job.FAILING_RESULTS):
            job.result = job_result
            job.voting = False
        test_buildset.jobs = test_jobs

        result = test_buildset.status
        expected = "Succeeding"
        self.assertEqual(result, expected)

    def test_status_wo_failing_and_voting_jobs_should_have_success_status(self):
        example_succeeding_job_results = ["SUCCESS", "SKIPPED"]

        test_buildset = fixtures.buildset()
        test_jobs = [fixtures.job()
                     for _ in example_succeeding_job_results]
        for job, job_result in zip(test_jobs,
                                   example_succeeding_job_results):
            job.result = job_result
        test_buildset.jobs = test_jobs

        result = test_buildset.status
        expected = "Succeeding"
        self.assertEqual(result, expected)

    def test_status_with_only_succeeding_voting_jobs_should_have_success(self):
        example_succeeding_job_results = ["SUCCESS", "SKIPPED"]

        test_buildset = fixtures.buildset()
        test_jobs = [fixtures.job() for _ in example_succeeding_job_results]
        for job, job_result in zip(test_jobs, example_succeeding_job_results):
            job.result = job_result
            job.voting = True
        test_buildset.jobs = test_jobs

        result = test_buildset.status
        expected = "Succeeding"
        self.assertEqual(result, expected)

    def test_status_with_mixed_non_voting_jobs_should_have_success_status(self):
        job_results = ["SUCCESS", "ERROR", "SKIPPED"]

        test_buildset = fixtures.buildset()
        test_jobs = [fixtures.job() for _ in job_results]

        for job, job_result in zip(test_jobs, job_results):
            job.result = job_result
            job.voting = False
        test_buildset.jobs = test_jobs

        result = test_buildset.status
        expected = "Succeeding"
        self.assertEqual(result, expected)

    def test_status_with_mixed_voting_jobs_should_have_fail_status(self):
        job_results = ["SUCCESS", "ERROR", "SKIPPED"]

        test_buildset = fixtures.buildset()
        test_jobs = [fixtures.job() for _ in job_results]

        for job, job_result in zip(test_jobs, job_results):
            job.result = job_result
            job.voting = True
        test_buildset.jobs = test_jobs

        result = test_buildset.status
        expected = "Failing"
        self.assertEqual(result, expected)

    def test_progress_wo_jobs_should_return_100(self):
        test_buildset = fixtures.buildset()
        test_buildset.jobs = []
        expected = 100
        result = test_buildset.progress
        self.assertEqual(result, expected)

    def test_progress_with_one_job_should_return_100(self):
        test_buildset = fixtures.buildset()
        test_job = fixtures.job()
        test_buildset.jobs = [test_job]
        expected = 100
        result = test_buildset.progress
        self.assertEqual(result, expected)

    def test_progress_with_multiple_jobs_should_return_expected(self):
        test_buildset = fixtures.buildset()
        test_jobs = [fixtures.job()
                     for x in range(3)]
        test_buildset.jobs = test_jobs
        expected = 100 / len(test_jobs)
        result = test_buildset.progress
        self.assertEqual(result, expected)

    def test_none_enqueue_should_return_none(self):
        test_buildset = fixtures.buildset()
        test_buildset.enqueue_time = None
        result = test_buildset.enqueue
        self.assertIsNone(result)

    def test_zero_enqueue_should_return_current_date(self):
        test_buildset = fixtures.buildset()
        test_buildset.enqueue_time = 0
        result = test_buildset.enqueue
        expected = epoch_to_datetime(0)
        self.assertEqual(result, expected)

    def test_valid_enqueue_should_return_expected(self):
        test_buildset = fixtures.buildset()
        result = test_buildset.enqueue
        expected = epoch_to_datetime(test_buildset.enqueue_time)
        self.assertEqual(result, expected)
