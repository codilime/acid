# -*- coding: utf-8 -*-
import unittest

from dashboard.time_utils import (epoch_to_datetime, milliseconds_to_seconds,
                                  seconds_to_time)


class TestTimeUtils(unittest.TestCase):
    def test_empty_epoch_to_datetime_should_raise_exception(self):
        with self.assertRaises(TypeError):
            epoch_to_datetime(seconds=None)

    def test_zero_epoch_to_datetime_should_return_data(self):
        result = epoch_to_datetime(seconds=0)
        expected = '1970-01-01 00:00:00 GMT'
        self.assertEqual(result, expected)

    def test_none_seconds_to_time_should_raise_excpetion(self):
        with self.assertRaises(TypeError):
            seconds_to_time(seconds=None)

    def test_one_hour_one_minute_one_second_to_time_should_return_data(self):
        result = seconds_to_time(seconds=3661)
        expected = '1:01:01'
        self.assertEqual(result, expected)

    def test_none_ms_milliseconds_to_seconds_should_raise_excpetion(self):
        with self.assertRaises(TypeError):
            milliseconds_to_seconds(milliseconds=None)

    def test_float_ms_milliseconds_to_seconds_should_return_data(self):
        result = milliseconds_to_seconds(milliseconds=8000.9)
        expected = 8.0
        self.assertEqual(result, expected)

    def test_int_ms_milliseconds_to_seconds_should_return_data(self):
        result = milliseconds_to_seconds(milliseconds=8000)
        expected = 8.0
        self.assertEqual(result, expected)
