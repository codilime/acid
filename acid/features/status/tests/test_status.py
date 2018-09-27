# -*- coding: utf-8 -*-
import pytest

from .. import model
from ..time_utils import (epoch_to_datetime, milliseconds_to_seconds,
                          seconds_to_time)


@pytest.mark.unit
@pytest.mark.status
class TestTimeTracker:
    def test_none_start_to_datetime_should_return_none(self, time_tracker):
        time_tracker.start = None
        assert time_tracker.start_to_datetime is None

    def test_none_elapsed_to_time_should_return_none(self, time_tracker):
        time_tracker.elapsed = None
        assert time_tracker.elapsed_to_time is None

    def test_none_remaining_to_time_should_return_none(self, time_tracker):
        time_tracker.remaining = None
        assert time_tracker.remaining_to_time is None

    def test_zero_remaining_to_time_should_return_zero(self, time_tracker):
        time_tracker.remaining = 0
        expected = seconds_to_time(0)
        assert time_tracker.remaining_to_time == expected

    def test_zero_start_to_datetime_should_return_data(self, time_tracker):
        expected = epoch_to_datetime(time_tracker.start)
        assert time_tracker.start_to_datetime == expected

    def test_hour_elapsed_to_time_should_return_data(self, time_tracker):
        expected = seconds_to_time(milliseconds_to_seconds(
            time_tracker.elapsed))
        assert time_tracker.elapsed_to_time == expected

    def test_hour_remaining_to_time_should_return_data(self, time_tracker):
        expected = seconds_to_time(milliseconds_to_seconds(
            time_tracker.remaining))
        assert time_tracker.remaining_to_time == expected


@pytest.mark.unit
@pytest.mark.status
class TestJob:
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

        expected_job = model.Job(name="test_name", result="test_result",
                                 url="http://fake_url",
                                 report_url="http://fake_url",
                                 canceled=False, voting=False, retry=False,
                                 worker={"name": "fake_name"},
                                 zuul_url="http://zuul_url",
                                 time_tracker=model.TimeTracker(start=1,
                                                                elapsed=1,
                                                                remaining=1,
                                                                estimated=1))

        return_job = model.Job.create(job=job_data, zuul_url="http://zuul_url")
        self._assert_jobs_equal(expected_job, return_job)

    def test_no_remaining_should_return_100(self, job):
        job.time_tracker.remaining = 0
        expected = 100
        assert job.progress == expected

    def test_no_estimated_should_return_0(self, job):
        job.time_tracker.estimated = 0
        expected = 0
        assert job.progress == expected

    def test_none_remaining_should_return_0(self, job):
        job.time_tracker.remaining = None
        expected = 0
        assert job.progress == expected

    def test_valid_progress_should_return_data(self, job):
        job.time_tracker.remaining = 1000
        job.time_tracker.estimated = 10
        expected = 90
        assert job.progress == expected

    def test_nonempty_result_should_return_data(self, job):
        job.result = "test"
        job.report_url = "http://fake_url"
        expected = "http://fake_url"
        assert job.log_url == expected

    @pytest.mark.parametrize("zuul_url", ['http://fake_url/////',
                                          'http://fake_url'])
    def test_empty_result_should_return_url_with_correct_slashes(self, zuul_url,
                                                                 job, mocker):
        job.result = None
        job._zuul_url = zuul_url
        job.url = "fake_endpoint"
        expected = "http://fake_url/fake_endpoint"
        assert job.log_url == expected

    def _assert_jobs_equal(self, job1, job2):
        assert job1.time_tracker.__dict__ == job2.time_tracker.__dict__
        job1.time_tracker = job2.time_tracker = None
        assert job1.__dict__ == job2.__dict__


@pytest.mark.unit
@pytest.mark.status
class TestBuildset:
    def _assert_buildset_equal(self, buildset1, buildset2):
        # assumes buildset has empty job list
        assert buildset1.owner == buildset2.owner
        buildset1.owner = buildset2.owner = None
        assert buildset1.__dict__ == buildset2.__dict__

    def test_create_should_return_expected_data(self, buildset):
        buildset_data = {"url": "http://fake_url",
                         "owner": {'name': 'John smith'}, "jobs": [],
                         "item_ahead": None, "live": True,
                         "remaining_time": 1812372, "failing_reasons": [],
                         "items_behind": [], "project": "test_name",
                         "id": "12345,6", "active": True, "zuul_ref": "12345",
                         "enqueue_time": 0}

        expected_buildset = buildset
        expected_buildset.enqueue_time = 0

        result_buildset = model.Buildset.create(buildset=buildset_data,
                                                zuul_url="http://zuul_url")

        self._assert_buildset_equal(expected_buildset, result_buildset)

    @pytest.mark.parametrize("enq_time", [None, 0])
    def test_no_enqueue_elapsed_time_should_return_0(self, enq_time, buildset):
        buildset.enqueue_time = enq_time
        expected = 0
        assert buildset.elapsed_time == expected

    def test_valid_elapsed_time_should_return_expected_time(self, buildset,
                                                            mocker):
        time = mocker.patch.object(model, 'time')
        fixed_time = 1532004145.20974
        time.return_value = fixed_time
        expected = seconds_to_time(fixed_time - buildset.enqueue_time)
        assert buildset.elapsed_time == expected

    def test_remaining_wo_jobs_should_return_none(self, buildset):
        buildset.jobs = []
        assert buildset.remaining_time is None

    def test_remaining_with_job_wo_remaining_should_return_none(self, job,
                                                                buildset):
        job.time_tracker.remaining = None
        buildset.jobs = [job]
        assert buildset.remaining_time is None

    def test_remaining_wh_multiple_jobs_should_return_longest_time(
        self, buildset, jobs):
        test_jobs = jobs(3)
        max_time = max(job.time_tracker.remaining for job in test_jobs)
        buildset.jobs = test_jobs

        expected = seconds_to_time(milliseconds_to_seconds(max_time))
        assert buildset.remaining_time == expected

    def test_start_wo_jobs_should_return_none(self, buildset):
        buildset.jobs = []
        assert buildset.start_datetime is None

    def test_start_with_job_wo_start_should_return_none(self, buildset, job):
        job.time_tracker.start = None
        buildset.jobs = [job]
        assert buildset.start_datetime is None

    def test_start_with_multiple_job_should_return_earliest_time(self, buildset,
                                                                 jobs):
        test_jobs = jobs(3)
        min_time = min(job.time_tracker.start for job in test_jobs)
        buildset.jobs = test_jobs
        expected = epoch_to_datetime(min_time)
        assert buildset.start_datetime == expected

    def test_status_wo_jobs_should_have_enqueued_status(self, buildset):
        buildset.jobs = []
        expected = 'Enqueued'
        assert buildset.status == expected

    @pytest.mark.parametrize("failing", model.Job.FAILING_RESULTS)
    def test_status_wh_any_failing_voting_job_should_have_fail_status(
            self, failing, job, buildset):
        job.voting = True
        job.result = failing
        buildset.jobs = [job]

        expected = "Failing"
        assert buildset.status == expected

    def test_status_with_failing_non_voting_job_should_success(self, buildset,
                                                               jobs):
        test_jobs = jobs(len(model.Job.FAILING_RESULTS))
        for job, job_result in zip(test_jobs, model.Job.FAILING_RESULTS):
            job.result = job_result
            job.voting = False
        buildset.jobs = test_jobs

        expected = "Succeeding"
        assert buildset.status == expected

    def test_status_wo_failing_and_voting_jobs_should_have_success_status(
            self, buildset, jobs):
        example_succeeding_job_results = ["SUCCESS", "SKIPPED"]

        test_jobs = jobs(len(example_succeeding_job_results))
        for job, job_result in zip(test_jobs, example_succeeding_job_results):
            job.result = job_result
        buildset.jobs = test_jobs

        expected = "Succeeding"
        assert buildset.status == expected

    def test_status_with_only_succeeding_voting_jobs_should_have_success(
            self, buildset, jobs):
        example_succeeding_job_results = ["SUCCESS", "SKIPPED"]

        test_jobs = jobs(len(example_succeeding_job_results))
        for job, job_result in zip(test_jobs, example_succeeding_job_results):
            job.result = job_result
            job.voting = True
        buildset.jobs = test_jobs

        expected = "Succeeding"
        assert buildset.status == expected

    def test_status_with_mixed_non_voting_jobs_should_have_success_status(
            self, buildset, jobs):
        job_results = ["SUCCESS", "ERROR", "SKIPPED"]

        test_jobs = jobs(len(job_results))
        for job, job_result in zip(test_jobs, job_results):
            job.result = job_result
            job.voting = False
        buildset.jobs = test_jobs

        expected = "Succeeding"
        assert buildset.status == expected

    def test_status_with_mixed_voting_jobs_should_have_fail_status(
            self, buildset, jobs):
        job_results = ["SUCCESS", "ERROR", "SKIPPED"]

        test_jobs = jobs(len(job_results))
        for job, job_result in zip(test_jobs, job_results):
            job.result = job_result
            job.voting = True
        buildset.jobs = test_jobs

        expected = "Failing"
        assert buildset.status == expected

    def test_progress_wo_jobs_should_return_100(self, buildset):
        buildset.jobs = []
        expected = 100
        assert buildset.progress == expected

    def test_progress_with_one_job_should_return_100(self, buildset, job):
        buildset.jobs = [job]
        expected = 100
        assert buildset.progress == expected

    def test_progress_with_multiple_jobs_should_return_expected(self, buildset,
                                                                jobs):
        test_jobs = jobs(3)
        buildset.jobs = test_jobs
        expected = 100 / len(test_jobs)
        assert buildset.progress == expected

    def test_none_enqueue_should_return_none(self, buildset):
        buildset.enqueue_time = None
        assert buildset.enqueue is None

    def test_zero_enqueue_should_return_current_date(self, buildset):
        buildset.enqueue_time = 0
        expected = epoch_to_datetime(0)
        assert buildset.enqueue == expected

    def test_valid_enqueue_should_return_expected(self, buildset):
        expected = epoch_to_datetime(buildset.enqueue_time)
        assert buildset.enqueue == expected

    def test_buildset_return_len(self, buildset):
        test_buildset = buildset
        test_buildset.jobs = ['master', 'gimp']
        assert len(test_buildset) == 2


@pytest.mark.unit
@pytest.mark.status
class TestQueue:
    def test_queue_should_return_valid_queue(self, queue):
        test_queue = queue
        buildsets_ref = [build.ref for build in test_queue.buildsets]
        expected = ['Z22c73722a05a41d7afe5580c46896f75',
                    'Z87136569311342c2a1fe4dd556ef6a39',
                    'Z75c2d6f5e9834689a58bf8d476b98ff2']
        assert buildsets_ref == expected

    def test_queue_return_len(self, queue):
        test_queue = queue
        assert len(test_queue) == 3
