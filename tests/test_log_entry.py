"""
Unit tests for LogEntry model
"""

import pytest
from datetime import datetime
from src.models.log_entry import LogEntry


class TestLogEntryJSON:
    """Test LogEntry with JSON format logs"""

    def test_parse_json_log_complete(self):
        """Test parsing JSON log with all fields"""
        log_line = '{"timestamp": "2024-01-20T10:30:45Z", "level": "INFO", "method": "GET", "path": "/api/users", "status": 200, "response_time": 45.2, "message": "Success"}'
        entry = LogEntry(log_line, 1)

        assert entry.level == "INFO"
        assert entry.method == "GET"
        assert entry.endpoint == "/api/users"
        assert entry.status_code == 200
        assert entry.response_time == 45.2
        assert entry.json_data is not None

    def test_parse_json_log_minimal(self):
        """Test parsing JSON log with minimal fields"""
        log_line = '{"level": "ERROR", "message": "Something went wrong"}'
        entry = LogEntry(log_line, 1)

        assert entry.level == "ERROR"
        assert "Something went wrong" in entry.message


class TestLogEntryText:
    """Test LogEntry with text format logs"""

    def test_parse_text_log_standard(self):
        """Test parsing standard text log format"""
        log_line = "2024-01-20 10:30:45 INFO GET /api/users 200 45ms"
        entry = LogEntry(log_line, 1)

        assert entry.level == "INFO"
        assert entry.method == "GET"
        assert entry.endpoint == "/api/users"
        assert entry.status_code == 200
        assert entry.response_time == 45.0

    def test_parse_text_log_with_brackets(self):
        """Test parsing text log with bracket format"""
        log_line = "[2024-01-20T10:30:45Z] ERROR POST /api/orders status=500 time=120ms"
        entry = LogEntry(log_line, 1)

        assert entry.level == "ERROR"
        assert entry.method == "POST"
        assert entry.endpoint == "/api/orders"
        assert entry.status_code == 500


class TestLogEntryColors:
    """Test color coding functionality"""

    def test_level_colors(self):
        """Test log level color mapping"""
        levels = {
            'DEBUG': 'cyan',
            'INFO': 'green',
            'ERROR': 'red',
            'WARN': 'yellow',
        }

        for level, expected_color in levels.items():
            log_line = f'{{"level": "{level}"}}'
            entry = LogEntry(log_line, 1)
            assert entry.get_level_color() == expected_color

    def test_status_code_colors(self):
        """Test status code color mapping"""
        test_cases = [
            (200, 'green'),
            (301, 'blue'),
            (404, 'yellow'),
            (500, 'red'),
        ]

        for status, expected_color in test_cases:
            log_line = f'{{"status": {status}}}'
            entry = LogEntry(log_line, 1)
            assert entry.get_status_color() == expected_color