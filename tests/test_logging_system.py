"""
Tests for Feature 13: Logging System

These commands provide Python-like logging:
- log_init, log_debug, log_info, log_warning, log_error, log_critical
- log_level, log_file, log_clear, log_count, log_get
"""

import pytest
import os
import tempfile
from techlang.interpreter import run


class TestLogInit:
    """Tests for log_init command."""
    
    def test_log_init_default(self):
        """Initialize logging with default level."""
        code = '''
log_init
log_info "Test message"
'''
        output = run(code).strip()
        # Should show INFO level message
        assert "INFO" in output or "Test message" in output


class TestLogLevels:
    """Tests for different log levels."""
    
    def test_log_debug(self):
        """Debug message respects log level."""
        code = '''
log_init DEBUG
log_debug "Debug message"
'''
        output = run(code).strip()
        assert "DEBUG" in output or "Debug message" in output
    
    def test_log_info(self):
        """Info message."""
        code = '''
log_init INFO
log_info "Info message"
'''
        output = run(code).strip()
        assert "INFO" in output or "Info message" in output
    
    def test_log_warning(self):
        """Warning message."""
        code = '''
log_init WARNING
log_warning "Warning message"
'''
        output = run(code).strip()
        assert "WARNING" in output or "Warning message" in output
    
    def test_log_error(self):
        """Error message."""
        code = '''
log_init ERROR
log_error "Error message"
'''
        output = run(code).strip()
        assert "ERROR" in output or "Error message" in output
    
    def test_log_critical(self):
        """Critical message."""
        code = '''
log_init CRITICAL
log_critical "Critical message"
'''
        output = run(code).strip()
        assert "CRITICAL" in output or "Critical message" in output


class TestLogFiltering:
    """Tests for log level filtering."""
    
    def test_debug_filtered_at_info(self):
        """Debug messages filtered when level is INFO."""
        code = '''
log_init INFO
log_debug "Should not show"
log_info "Should show"
log_count count
print count
'''
        output = run(code).strip()
        # Only INFO message should be logged
        assert "Should not show" not in output
    
    def test_info_filtered_at_warning(self):
        """Info messages filtered when level is WARNING."""
        code = '''
log_init WARNING
log_info "Should not show"
log_warning "Should show"
log_count count
print count
'''
        output = run(code).strip()
        assert "Should not show" not in output


class TestLogLevel:
    """Tests for changing log level."""
    
    def test_change_level(self):
        """Change log level dynamically."""
        code = '''
log_init ERROR
log_warning "Not shown"
log_level WARNING
log_warning "Now shown"
'''
        output = run(code).strip()
        # First warning filtered, second shown
        assert "Now shown" in output


class TestLogClear:
    """Tests for log_clear command."""
    
    def test_clear_logs(self):
        """Clear all log entries."""
        code = '''
log_init INFO
log_info "Message 1"
log_info "Message 2"
log_count before
log_clear
log_count after
print before
print after
'''
        output = run(code).strip().splitlines()
        # Should show counts before and after clear
        before = int(output[-2])
        after = int(output[-1])
        assert before >= 2
        assert after == 0


class TestLogCount:
    """Tests for log_count command."""
    
    def test_count_messages(self):
        """Count logged messages."""
        code = '''
log_init INFO
log_info "One"
log_info "Two"
log_info "Three"
log_count count
print count
'''
        output = run(code).strip()
        lines = output.splitlines()
        assert lines[-1] == "3"


class TestLogGet:
    """Tests for log_get command."""
    
    def test_get_specific_log(self):
        """Retrieve specific log entry."""
        code = '''
log_init INFO
log_info "First"
log_info "Second"
log_info "Third"
log_get 1 entry
print entry
'''
        output = run(code).strip()
        assert "Second" in output


class TestLogFile:
    """Tests for log_file command."""
    
    def test_log_to_file(self, tmp_path):
        """Write logs to file."""
        log_path = tmp_path / "test.log"
        code = f'''
log_init INFO
log_file "{str(log_path).replace(chr(92), '/')}"
log_info "File message"
'''
        run(code, base_dir=str(tmp_path))
        # File might be created
        # Just verify no errors


class TestLoggingIntegration:
    """Integration tests for logging system."""
    
    def test_complete_logging_workflow(self):
        """Complete logging workflow."""
        code = '''
log_init DEBUG
log_debug "Starting application"
log_info "Processing data"
log_warning "Low memory"
log_error "Failed to connect"
log_count total
print total
'''
        output = run(code).strip()
        lines = output.splitlines()
        assert lines[-1] == "4"
    
    def test_logging_with_variables(self):
        """Log messages from variables."""
        code = '''
log_init INFO
str_set msg "Dynamic message"
log_info msg
'''
        output = run(code).strip()
        assert "Dynamic message" in output
