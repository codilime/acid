# -*- coding: utf-8 -*-
from unittest import TestCase
from unittest.mock import MagicMock, patch

import acid.features.status.service
import acid.features.status.tests.fixtures
from acid.config import config
from acid.features.status.exceptions import (PipelineNotFound,
                                             RemoteServerError)
from acid.features.status.model import PipelineStat


class TestServicePipelineStats(TestCase):
    def test_pipelines_stats_returns_empty_when_no_pipelines(self):
        resource = acid.features.status.tests.fixtures.load_status_data(
            name='status_no_pipelines')
        expected = []
        result = acid.features.status.service.pipelines_stats(
            pipelines=resource['pipelines'])
        self.assertEqual(result, expected)

    def test_pipelines_stats_returns_zeros_for_empty_pipelines(self):
        resource = acid.features.status.tests.fixtures.load_status_data(
            name='status_pipelines_with_no_buildsets')
        result = acid.features.status.service.pipelines_stats(
            pipelines=resource['pipelines'])
        expected = [PipelineStat(name='check', buildsets_count=0),
                    PipelineStat(name='gate', buildsets_count=0)]
        self.assertEqual(result, expected)

    def test_pipelines_stats_returns_nothing_for_pipelines_not_in_config(self):
        resource = acid.features.status.tests.fixtures.load_status_data(
            name='status_pipelines_not_on_list_in_config')
        result = acid.features.status.service.pipelines_stats(
            pipelines=resource['pipelines'])
        expected = [PipelineStat(name='check', buildsets_count=0)]
        self.assertEqual(result, expected)

    def test_pipelines_stats_returns_expected_for_queue_with_many_heads(self):
        resource = acid.features.status.tests.fixtures.load_status_data(
            name='status_pipeline_with_couple_buildsets_in_queue')
        result = acid.features.status.service.pipelines_stats(
            pipelines=resource['pipelines'])
        expected = [PipelineStat(name='check', buildsets_count=3)]
        self.assertEqual(result, expected)


class TestServiceEndpointStatus(TestCase):
    def test_status_endpoint_returns_expected_when_no_slashes(self):
        with patch.dict(config['zuul'], {'url': 'http://fake.url',
                                         'status_endpoint': 'fake.json'}):
            result = acid.features.status.service.status_endpoint()
            expected = 'http://fake.url/fake.json'
            self.assertEqual(result, expected)

    def test_status_endpoint_returns_expected_when_one_slash(self):
        with patch.dict(config['zuul'], {'url': 'http://fake.url/',
                                         'status_endpoint': 'fake.json'}):
            result = acid.features.status.service.status_endpoint()
            expected = 'http://fake.url/fake.json'
            self.assertEqual(result, expected)

    def test_status_endpoint_returns_expected_when_multiple_slashes(self):
        with patch.dict(config['zuul'], {'url': 'http://fake.url////////////',
                                         'status_endpoint': 'fake.json'}):
            result = acid.features.status.service.status_endpoint()
            expected = 'http://fake.url/fake.json'
            self.assertEqual(result, expected)


@patch('acid.features.status.service.current_app')
@patch('acid.features.status.service.requests')
class TestServiceFetchData(TestCase):
    def test_fetch_raise_when_cant_download(self, requests, *args):
        result = MagicMock()
        result.status_code = 404
        result.text = "{}"
        requests.get.return_value = result
        with self.assertRaises(RemoteServerError):
            acid.features.status.service.fetch_json_data(
                endpoint='http://fake.endpoint')

    def test_fetch_return_expected_data(self, requests, *args):
        requests.get = acid.features.status.tests.fixtures.status_request(
            filename='status_check')

        result = acid.features.status.service.fetch_json_data(
            endpoint='http://fake.endpoint')
        expected = acid.features.status.tests.fixtures.load_status_data(
            name='status_check')
        self.assertDictEqual(result, expected)


@patch('acid.features.status.service.current_app')
class TestServiceMakeQueues(TestCase):
    def test_raises_when_no_queues(self, *args):
        resources = acid.features.status.tests.fixtures.load_status_data(
            name='status_no_queues')
        with self.assertRaises(KeyError):
            acid.features.status.service.make_queues(
                pipelines=resources['pipelines'], pipename='check')

    def test_raises_when_no_pipeline(self, *args):
        resources = acid.features.status.tests.fixtures.load_status_data(
            name='status_no_pipelines')
        with self.assertRaises(PipelineNotFound):
            acid.features.status.service.make_queues(
                pipelines=resources['pipelines'], pipename='check')
