# -*- coding: utf-8 -*-
import unittest
from unittest.mock import MagicMock, patch

from tests import fixtures

from dashboard import service
from dashboard.config import config
from dashboard.exceptions import PipelineNotFound, RemoteServerError
from dashboard.status import PipelineStat


class TestServicePipelineStats(unittest.TestCase):
    def test_pipelines_stats_returns_empty_when_no_pipelines(self):
        resource = fixtures.load_status_data(name='status_no_pipelines')
        expected = []
        result = service.pipelines_stats(pipelines=resource['pipelines'])
        self.assertEqual(result, expected)

    def test_pipelines_stats_returns_zeros_for_empty_pipelines(self):
        resource = fixtures.load_status_data(
            name='status_pipelines_with_no_buildsets')
        result = service.pipelines_stats(pipelines=resource['pipelines'])
        expected = [PipelineStat(name='test_pipeline1', buildsets_count=0),
                    PipelineStat(name='test_pipeline2', buildsets_count=0)]
        self.assertEqual(result, expected)

    def test_pipelines_stats_returns_expected_for_queue_with_many_heads(self):
        resource = fixtures.load_status_data(
            name='status_pipeline_with_couple_buildsets_in_queue')
        result = service.pipelines_stats(pipelines=resource['pipelines'])
        expected = [PipelineStat(name='test_pipeline1', buildsets_count=3)]
        self.assertEqual(result, expected)


class TestServiceEndpointStatus(unittest.TestCase):
    def test_status_endpoint_returns_expected_when_no_slashes(self):
        with patch.dict(config['zuul'], {'url': 'http://fake.url',
                                         'status_endpoint': 'fake.json'}):
            result = service.status_endpoint()
            expected = 'http://fake.url/fake.json'
            self.assertEqual(result, expected)

    def test_status_endpoint_returns_expected_when_one_slash(self):
        with patch.dict(config['zuul'], {'url': 'http://fake.url/',
                                         'status_endpoint': 'fake.json'}):
            result = service.status_endpoint()
            expected = 'http://fake.url/fake.json'
            self.assertEqual(result, expected)

    def test_status_endpoint_returns_expected_when_multiple_slashes(self):
        with patch.dict(config['zuul'], {'url': 'http://fake.url////////////',
                                         'status_endpoint': 'fake.json'}):
            result = service.status_endpoint()
            expected = 'http://fake.url/fake.json'
            self.assertEqual(result, expected)


@patch('dashboard.service.current_app')
@patch('dashboard.service.requests')
class TestServiceFetchData(unittest.TestCase):
    def test_fetch_reise_when_cant_download(self, requests, *args):
        result = MagicMock()
        result.status_code = 404
        result.text = "{}"
        requests.get.return_value = result
        with self.assertRaises(RemoteServerError):
            service.fetch_json_data(endpoint='http://fake.endpoint')

    def test_fetch_return_expected_data(self, requests, *args):
        requests.get = fixtures.status_request(
            filename='tests/static/status_check.json')

        result = service.fetch_json_data(endpoint='http://fake.endpoint')
        expected = fixtures.load_status_data(name='status_check')
        self.assertDictEqual(result, expected)


@patch('dashboard.service.current_app')
class TestServiceMakeQueues(unittest.TestCase):
    def test_raises_when_no_queues(self, *args):
        resources = fixtures.load_status_data(name='status_no_queues')
        with self.assertRaises(KeyError):
            service.make_queues(
                pipelines=resources['pipelines'], pipename='check')

    def test_raises_when_no_pipeline(self, *args):
        resources = fixtures.load_status_data(name='status_no_pipelines')
        with self.assertRaises(PipelineNotFound):
            service.make_queues(
                pipelines=resources['pipelines'], pipename='check')
