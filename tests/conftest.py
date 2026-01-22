"""
Pytest configuration and fixtures
"""

import pytest


@pytest.fixture(scope="session")
def sample_logs():
    """Sample log entries for testing"""
    return [
        '{"timestamp": "2024-01-20T10:30:45Z", "level": "INFO", "method": "GET", "path": "/api/users", "status": 200}',
        '2024-01-20 10:30:46 ERROR POST /api/orders 500 120ms',
        '[2024-01-20T10:30:47Z] WARN GET /api/products status=404',
    ]