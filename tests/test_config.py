# -*- coding: utf-8 -*-
import os
import unittest

from dashboard.config import Config


class TestConfig(unittest.TestCase):
    def test_config_object_can_be_created(self):
        Config(file_path='tests/test_settings.yml')

    def test_config_raises_when_file_path_does_not_exist(self):
        with self.assertRaises(FileNotFoundError):
            Config(file_path='/fake/path/settings.yml')

    def test_config_can_be_created_with_file_path_expect_types(self):
        Config(file_path='tests/test_settings.yml')
        Config(file_path=os.path.normpath('tests/test_settings.yml'))
        Config(file_path=b'tests/test_settings.yml')

    def test_config_raises_when_file_path_is_unexpected_type(self):
        with self.assertRaises(TypeError):
            Config(file_path=124234)

    def test_config_should_be_dict_like(self):
        config = Config(file_path='tests/test_settings.yml')
        self.assertIn('default', config)
        self.assertTrue(hasattr(config, 'get'))

        config['default']['pipeline'] = 'test-pipeline'
        self.assertDictEqual(config['default'],
                             {'pipeline': 'test-pipeline'})

    def test_config_raises_when_try_to_set_new_section(self):
        config = Config(file_path='tests/test_settings.yml')
        with self.assertRaises(TypeError):
            config['new_section'] = {'test': 'foo'}
