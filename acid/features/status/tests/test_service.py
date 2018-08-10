# -*- coding: utf-8 -*-
import unittest
from unittest.mock import MagicMock, patch

from .. import service
from . import fixtures

from acid.config import config

from ..exceptions import PipelineNotFound, RemoteServerError
from ..model import PipelineStat


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
        expected = [PipelineStat(name='check', buildsets_count=0),
                    PipelineStat(name='gate', buildsets_count=0)]
        self.assertEqual(result, expected)

    def test_pipelines_stats_returns_nothing_for_pipelines_not_in_config(self):
        resource = fixtures.load_status_data(
            name='status_pipelines_not_on_list_in_config')
        result = service.pipelines_stats(pipelines=resource['pipelines'])
        expected = [PipelineStat(name='check', buildsets_count=0)]
        self.assertEqual(result, expected)

    def test_pipelines_stats_returns_expected_for_queue_with_many_heads(self):
        resource = fixtures.load_status_data(
            name='status_pipeline_with_couple_buildsets_in_queue')
        result = service.pipelines_stats(pipelines=resource['pipelines'])
        expected = [PipelineStat(name='check', buildsets_count=3)]
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


@patch('acid.features.status.service.current_app')
@patch('acid.features.status.service.requests')
class TestServiceFetchData(unittest.TestCase):
    def test_fetch_raise_when_cant_download(self, requests, *args):
        result = MagicMock()
        result.status_code = 404
        result.text = "{}"
        requests.get.return_value = result
        with self.assertRaises(RemoteServerError):
            service.fetch_json_data(endpoint='http://fake.endpoint')

    def test_fetch_return_expected_data(self, requests, *args):
        requests.get = fixtures.status_request(filename='status_check')
        result = service.fetch_json_data(endpoint='http://fake.endpoint')
        expected = fixtures.load_status_data(name='status_check')
        self.assertDictEqual(result, expected)


@patch('acid.features.status.service.current_app')
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
