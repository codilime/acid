# -*- coding: utf-8 -*-
import os

import pytest

from acid.config import Config


@pytest.mark.unit
class TestConfig:
    def test_config_object_can_be_created(self):
        Config(file_path=os.getenv('SETTINGS_PATH'))

    def test_config_raises_when_file_path_does_not_exist(self):
        with pytest.raises(FileNotFoundError):
            Config(file_path='/fake/path/settings.yml')

    def test_config_can_be_created_with_file_path_expect_types(self):
        Config(file_path=os.getenv('SETTINGS_PATH'))
        Config(file_path=os.path.normpath(os.getenv('SETTINGS_PATH')))
        Config(file_path=bytes(os.getenv('SETTINGS_PATH'), encoding="utf-8"))

    def test_config_raises_when_file_path_is_unexpected_type(self):
        with pytest.raises(TypeError):
            Config(file_path=124234)

    def test_config_should_be_dict_like(self):
        config = Config(file_path=os.getenv('SETTINGS_PATH'))
        assert 'default' in config
        assert hasattr(config, 'get')

        expected = {'pipename': 'periodic-nightly',
                    'users_file': 'users_test.yml',
                    'secret_key': 'thisisverysecret',
                    'openid_provider': 'https://login.launchpad.net/+openid'}
        # check only subset of config file to avoid bloating test source code
        assert config['default'] == expected

    def test_config_raises_when_try_to_set_new_section(self):
        config = Config(file_path=os.getenv('SETTINGS_PATH'))
        with pytest.raises(TypeError):
            config['new_section'] = {'test': 'foo'}
