"""
Unit tests for LogViewer class
"""

import pytest
import tempfile
from pathlib import Path
from src.log_viewer import LogViewer


class TestLogViewer:
    """Test LogViewer functionality"""

    @pytest.fixture
    def sample_log_file(self):
        """Create a temporary log file for testing"""
        content = """2024-01-20 10:30:45 INFO GET /api/users 200 45ms
2024-01-20 10:30:46 ERROR POST /api/orders 500 120ms
{"timestamp": "2024-01-20T10:30:47Z", "level": "WARN", "method": "GET", "status": 404}
"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.log') as f:
            f.write(content)
            return f.name

    def test_load_file(self, sample_log_file):
        """Test loading and parsing log file"""
        viewer = LogViewer(sample_log_file)
        viewer.load()

        assert len(viewer.entries) == 3
        assert len(viewer.filtered_entries) == 3

    def test_filter_by_level(self, sample_log_file):
        """Test filtering by log level"""
        viewer = LogViewer(sample_log_file)
        viewer.load()
        viewer.filter_logs(level='ERROR')

        assert len(viewer.filtered_entries) == 1
        assert viewer.filtered_entries[0].level == 'ERROR'

    def test_filter_by_method(self, sample_log_file):
        """Test filtering by HTTP method"""
        viewer = LogViewer(sample_log_file)
        viewer.load()
        viewer.filter_logs(method='GET')

        assert len(viewer.filtered_entries) == 2
        for entry in viewer.filtered_entries:
            assert entry.method == 'GET'

    def test_filter_by_status(self, sample_log_file):
        """Test filtering by status code"""
        viewer = LogViewer(sample_log_file)
        viewer.load()
        viewer.filter_logs(status_code=500)

        assert len(viewer.filtered_entries) == 1
        assert viewer.filtered_entries[0].status_code == 500

    def test_clear_filters(self, sample_log_file):
        """Test clearing filters"""
        viewer = LogViewer(sample_log_file)
        viewer.load()
        viewer.filter_logs(level='ERROR')
        assert len(viewer.filtered_entries) == 1

        viewer.clear_filters()
        assert len(viewer.filtered_entries) == 3