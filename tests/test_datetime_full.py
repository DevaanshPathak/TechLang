"""
Tests for Date/Time Full Support

These commands provide comprehensive datetime functionality:
- datetime_now, datetime_utc
- datetime_parse, datetime_format
- datetime_add, datetime_diff
- datetime_weekday, datetime_timestamp, datetime_from_timestamp
"""

import pytest
from techlang.interpreter import run


class TestDateTimeNow:
    """Tests for datetime_now command."""
    
    def test_datetime_now_creates_datetime(self):
        """datetime_now creates a datetime object."""
        code = '''
datetime_now dt
print dt
'''
        output = run(code).strip()
        # Should contain date-like format
        assert "-" in output  # ISO format has dashes
    
    def test_datetime_now_format(self):
        """datetime_now can be formatted."""
        code = '''
datetime_now dt
datetime_format dt "%Y" year_str
print year_str
'''
        output = run(code).strip()
        # Should be a 4-digit year like 2024 or 2025
        assert len(output) == 4
        assert output.isdigit()


class TestDateTimeUTC:
    """Tests for datetime_utc command."""
    
    def test_datetime_utc_creates_datetime(self):
        """datetime_utc creates a UTC datetime object."""
        code = '''
datetime_utc dt
print dt
'''
        output = run(code).strip()
        assert "-" in output


class TestDateTimeParse:
    """Tests for datetime_parse command."""
    
    def test_parse_iso_format(self):
        """Parse ISO format datetime."""
        code = '''
str_create datestr "2024-06-15 14:30:00"
datetime_parse datestr "%Y-%m-%d %H:%M:%S" dt
datetime_format dt "%Y" year
print year
'''
        output = run(code).strip().splitlines()
        assert output[-1] == "2024"
    
    def test_parse_custom_format(self):
        """Parse custom format datetime."""
        code = '''
str_create datestr "15/06/2024"
datetime_parse datestr "%d/%m/%Y" dt
datetime_format dt "%Y-%m-%d" result
print result
'''
        output = run(code).strip().splitlines()
        assert output[-1] == "2024-06-15"


class TestDateTimeFormat:
    """Tests for datetime_format command."""
    
    def test_format_full(self):
        """Format datetime with full pattern."""
        code = '''
str_create datestr "2024-06-15 14:30:00"
datetime_parse datestr "%Y-%m-%d %H:%M:%S" dt
datetime_format dt "%B %d, %Y" result
print result
'''
        output = run(code).strip().splitlines()
        assert output[-1] == "June 15, 2024"
    
    def test_format_time_only(self):
        """Format time component only."""
        code = '''
str_create datestr "2024-06-15 14:30:45"
datetime_parse datestr "%Y-%m-%d %H:%M:%S" dt
datetime_format dt "%H:%M:%S" result
print result
'''
        output = run(code).strip().splitlines()
        assert output[-1] == "14:30:45"


class TestDateTimeAdd:
    """Tests for datetime_add command."""
    
    def test_add_days(self):
        """Add days to datetime."""
        code = '''
str_create datestr "2024-06-15"
datetime_parse datestr "%Y-%m-%d" dt
datetime_add dt 5 days new_dt
datetime_format new_dt "%Y-%m-%d" result
print result
'''
        output = run(code).strip().splitlines()
        assert output[-1] == "2024-06-20"
    
    def test_add_hours(self):
        """Add hours to datetime."""
        code = '''
str_create datestr "2024-06-15 10:00:00"
datetime_parse datestr "%Y-%m-%d %H:%M:%S" dt
datetime_add dt 3 hours new_dt
datetime_format new_dt "%H" hour
print hour
'''
        output = run(code).strip().splitlines()
        assert output[-1] == "13"
    
    def test_add_negative(self):
        """Subtract by adding negative."""
        code = '''
str_create datestr "2024-06-15"
datetime_parse datestr "%Y-%m-%d" dt
datetime_add dt -5 days new_dt
datetime_format new_dt "%Y-%m-%d" result
print result
'''
        output = run(code).strip().splitlines()
        assert output[-1] == "2024-06-10"


class TestDateTimeDiff:
    """Tests for datetime_diff command."""
    
    def test_diff_days(self):
        """Calculate difference in days."""
        code = '''
str_create date1 "2024-06-15"
str_create date2 "2024-06-20"
datetime_parse date1 "%Y-%m-%d" dt1
datetime_parse date2 "%Y-%m-%d" dt2
datetime_diff dt2 dt1 days diff
print diff
'''
        output = run(code).strip().splitlines()
        assert output[-1] == "5"
    
    def test_diff_hours(self):
        """Calculate difference in hours."""
        code = '''
str_create date1 "2024-06-15 10:00:00"
str_create date2 "2024-06-15 14:30:00"
datetime_parse date1 "%Y-%m-%d %H:%M:%S" dt1
datetime_parse date2 "%Y-%m-%d %H:%M:%S" dt2
datetime_diff dt2 dt1 hours diff
print diff
'''
        output = run(code).strip().splitlines()
        assert output[-1] == "4"  # 4.5 hours truncated to 4


class TestDateTimeWeekday:
    """Tests for datetime_weekday command."""
    
    def test_weekday_saturday(self):
        """Get weekday for known date (Saturday)."""
        code = '''
str_create datestr "2024-06-15"
datetime_parse datestr "%Y-%m-%d" dt
datetime_weekday dt day
print day
'''
        output = run(code).strip().splitlines()
        assert output[-1] == "Saturday"
    
    def test_weekday_monday(self):
        """Get weekday for known date (Monday)."""
        code = '''
str_create datestr "2024-06-10"
datetime_parse datestr "%Y-%m-%d" dt
datetime_weekday dt day
print day
'''
        output = run(code).strip().splitlines()
        assert output[-1] == "Monday"


class TestDateTimeTimestamp:
    """Tests for datetime_timestamp and datetime_from_timestamp."""
    
    def test_timestamp_round_trip(self):
        """Convert to timestamp and back."""
        code = '''
str_create datestr "2024-06-15 12:00:00"
datetime_parse datestr "%Y-%m-%d %H:%M:%S" dt1
datetime_timestamp dt1 ts
datetime_from_timestamp ts dt2
datetime_format dt2 "%Y-%m-%d %H:%M:%S" result
print result
'''
        output = run(code).strip().splitlines()
        assert output[-1] == "2024-06-15 12:00:00"
    
    def test_timestamp_value(self):
        """Timestamp is a numeric value."""
        code = '''
str_create datestr "2024-06-15 12:00:00"
datetime_parse datestr "%Y-%m-%d %H:%M:%S" dt
datetime_timestamp dt ts
print ts
'''
        output = run(code).strip().splitlines()
        # Should be a large number (Unix timestamp)
        assert int(output[-1]) > 1700000000


class TestDateTimeIntegration:
    """Integration tests for datetime features."""
    
    def test_age_calculation(self):
        """Calculate age from birthdate."""
        code = '''
str_create birthdate "1990-05-20"
str_create today "2024-06-15"
datetime_parse birthdate "%Y-%m-%d" birth
datetime_parse today "%Y-%m-%d" now
datetime_diff now birth days diff
set years diff
div years 365
print years
'''
        output = run(code).strip().splitlines()
        # Should be about 34 years
        assert int(output[-1]) >= 34
    
    def test_deadline_check(self):
        """Check if a deadline has passed."""
        code = '''
str_create deadline_str "2024-06-20 17:00:00"
str_create current_str "2024-06-15 10:00:00"
datetime_parse deadline_str "%Y-%m-%d %H:%M:%S" deadline
datetime_parse current_str "%Y-%m-%d %H:%M:%S" current
datetime_diff deadline current days remaining
print remaining
'''
        output = run(code).strip().splitlines()
        assert int(output[-1]) == 5
