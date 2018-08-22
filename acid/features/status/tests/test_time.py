# -*- coding: utf-8 -*-
import pytest

from ..time_utils import (epoch_to_datetime, milliseconds_to_seconds,
                          seconds_to_time)


@pytest.mark.unit
class TestTimeUtils:
    def test_empty_epoch_to_datetime_should_raise_exception(self):
        with pytest.raises(TypeError):
            epoch_to_datetime(seconds=None)

    def test_zero_epoch_to_datetime_should_return_data(self):
        test_seconds = 0
        expected = '1970-01-01 00:00:00'
        assert epoch_to_datetime(seconds=test_seconds) == expected

    def test_none_seconds_to_time_should_raise_exception(self):
        with pytest.raises(TypeError):
            seconds_to_time(seconds=None)

    def test_one_hour_one_minute_one_second_to_time_should_return_data(self):
        test_seconds = 3661
        expected = '1:01:01'
        assert seconds_to_time(seconds=test_seconds) == expected

    def test_none_ms_milliseconds_to_seconds_should_raise_exception(self):
        with pytest.raises(TypeError):
            milliseconds_to_seconds(milliseconds=None)

    @pytest.mark.parametrize("test_time", [8000.9, 8000])
    def test_milliseconds_to_seconds_should_return_data(self, test_time):
        expected = 8.0
        assert milliseconds_to_seconds(milliseconds=test_time) == expected
