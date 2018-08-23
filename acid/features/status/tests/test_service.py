# -*- coding: utf-8 -*-
import pytest

from .. import service

from acid.tests import TestWithAppContext

from ..exceptions import PipelineNotFound, RemoteServerError
from ..model import PipelineStat


@pytest.mark.unit
class TestServicePipelineStats:
    def test_pipelines_stats_returns_empty_when_no_pipelines(self,
                                                             load_status_data):
        resource = load_status_data(name='status_no_pipelines')
        expected = []
        result = service.pipelines_stats(pipelines=resource['pipelines'],
                                         showed_pipelines=['check', 'gate'])
        assert result == expected

    def test_pipelines_stats_returns_zeros_for_empty_pipeline(self,
                                                              load_status_data):
        resource = load_status_data(name='status_pipelines_with_no_buildsets')
        result = service.pipelines_stats(pipelines=resource['pipelines'],
                                         showed_pipelines=['check', 'gate'])
        expected = [PipelineStat(name='check', buildsets_count=0),
                    PipelineStat(name='gate', buildsets_count=0)]
        assert result == expected

    def test_pipelines_stats_returns_nothing_for_pipelines_not_in_config(
            self, load_status_data):
        resource = load_status_data(
            name='status_pipelines_not_on_list_in_config')
        result = service.pipelines_stats(pipelines=resource['pipelines'],
                                         showed_pipelines=['check', 'gate'])
        expected = [PipelineStat(name='check', buildsets_count=0)]
        assert result == expected

    def test_pipelines_stats_returns_expected_for_queue_with_many_heads(
        self, load_status_data):
        resource = load_status_data(
            name='status_pipeline_with_couple_buildsets_in_queue')
        result = service.pipelines_stats(pipelines=resource['pipelines'],
                                         showed_pipelines=['check'])
        expected = [PipelineStat(name='check', buildsets_count=3)]
        assert result == expected


@pytest.mark.unit
class TestServiceEndpointStatus:
    def test_status_endpoint_returns_expected_when_no_slashes(self):
        result = service.status_endpoint(zuul_url='http://fake.url',
                                         zuul_endpoint='fake.json')
        expected = 'http://fake.url/fake.json'
        assert result == expected

    def test_status_endpoint_returns_expected_when_one_slash(self):
        result = service.status_endpoint(zuul_url='http://fake.url/',
                                         zuul_endpoint='fake.json')
        expected = 'http://fake.url/fake.json'
        assert result == expected

    def test_status_endpoint_returns_expected_when_multiple_slash(self):
        result = service.status_endpoint(zuul_url='http://fake.url////////////',
                                         zuul_endpoint='fake.json')
        expected = 'http://fake.url/fake.json'
        assert result == expected


@pytest.mark.unit
class TestServiceFetchData(TestWithAppContext):
    def test_fetch_raise_when_cant_download(self, mocker):
        requests = mocker.patch.object(service, 'requests')
        result = mocker.MagicMock()
        result.status_code = 404
        result.text = "{}"
        requests.get.return_value = result
        with pytest.raises(RemoteServerError):
            service.fetch_json_data(endpoint='http://fake.endpoint')

    def test_fetch_return_expected_data(self, status_request,
                                        load_status_data, mocker):
        requests = mocker.patch.object(service, 'requests')
        requests.get = status_request(filename='status_check')
        result = service.fetch_json_data(endpoint='http://fake.endpoint')
        expected = load_status_data(name='status_check')
        assert result == expected


@pytest.mark.unit
class TestServiceMakeQueues(TestWithAppContext):
    def test_raises_when_no_queues(self, load_status_data):
        resources = load_status_data(name='status_no_queues')
        with pytest.raises(KeyError):
            service.make_queues(pipelines=resources['pipelines'],
                                pipename='check')

    def test_raises_when_no_pipeline(self, load_status_data):
        resources = load_status_data(name='status_no_pipelines')
        with pytest.raises(PipelineNotFound):
            service.make_queues(pipelines=resources['pipelines'],
                                pipename='check')
