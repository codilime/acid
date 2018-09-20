# -*- coding: utf-8 -*-
import os

import pytest

from acid.yaml_utils import read_yaml


@pytest.mark.unit
class TestReadYaml:
    def test_settings_can_be_loaded(self):
        read_yaml(file_path=os.getenv('SETTINGS_PATH'))

    def test_reader_raises_when_file_path_does_not_exist(self):
        with pytest.raises(FileNotFoundError):
            read_yaml(file_path='/fake/path/settings.yml')

    def test_settings_can_be_loaded_from_file_path_expect_types(self):
        read_yaml(file_path=os.getenv('SETTINGS_PATH'))
        read_yaml(file_path=os.path.normpath(os.getenv('SETTINGS_PATH')))
        read_yaml(file_path=bytes(
            os.getenv('SETTINGS_PATH'), encoding="utf-8"))

    def test_reader_raises_when_file_path_is_unexpected_type(self):
        with pytest.raises(TypeError):
            read_yaml(file_path=124234)

    def test_settings_should_be_dict_like(self):
        settings = read_yaml(file_path=os.getenv('SETTINGS_PATH'))
        assert 'default' in settings
        assert hasattr(settings, 'get')

        expected = {'pipename': 'periodic-nightly',
                    'users_file': 'config/test/users_test.yml',
                    'secret_key': 'thisisverysecret'}
        # check only subset of config file to avoid bloating test source code
        assert settings['default'] == expected
