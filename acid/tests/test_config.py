# -*- coding: utf-8 -*-
import os
from unittest import TestCase

from acid.config import Config


class TestConfig(TestCase):
    def test_config_object_can_be_created(self):
        Config(file_path=os.getenv('SETTINGS_PATH'))

    def test_config_raises_when_file_path_does_not_exist(self):
        with self.assertRaises(FileNotFoundError):
            Config(file_path='/fake/path/settings.yml')

    def test_config_can_be_created_with_file_path_expect_types(self):
        Config(file_path=os.getenv('SETTINGS_PATH'))
        Config(file_path=os.path.normpath(os.getenv('SETTINGS_PATH')))
        Config(file_path=bytes(os.getenv('SETTINGS_PATH'),encoding="utf-8"))

    def test_config_raises_when_file_path_is_unexpected_type(self):
        with self.assertRaises(TypeError):
            Config(file_path=124234)

    def test_config_should_be_dict_like(self):
        config = Config(file_path=os.getenv('SETTINGS_PATH'))
        self.assertIn('default', config)
        self.assertTrue(hasattr(config, 'get'))

        config['default']['pipename'] = 'test-pipeline'
        config['default']['users_file'] = 'test_admins.yml'
        config['default']['secret_key'] = 'thisisverysecret'
        self.assertDictEqual(config['default'],
                             {'pipename': 'test-pipeline',
                              'users_file': 'test_admins.yml',
                              'secret_key': 'thisisverysecret',
                              'openid_provider':
                              'https://login.launchpad.net/+openid'})

    def test_config_raises_when_try_to_set_new_section(self):
        config = Config(file_path=os.getenv('SETTINGS_PATH'))
        with self.assertRaises(TypeError):
            config['new_section'] = {'test': 'foo'}
