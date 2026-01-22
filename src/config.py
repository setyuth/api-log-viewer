"""
Configuration settings for API Log Viewer
"""

# Display settings
DEFAULT_LIST_LIMIT = 50
MAX_ENDPOINT_LENGTH = 30
MAX_MESSAGE_LENGTH = 40

# Color schemes
LOG_LEVEL_COLORS = {
    'DEBUG': 'cyan',
    'INFO': 'green',
    'WARN': 'yellow',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'FATAL': 'bright_red',
    'CRITICAL': 'bright_red',
}

# HTTP status code color ranges
STATUS_CODE_COLORS = {
    'success': (200, 299, 'green'),
    'redirect': (300, 399, 'blue'),
    'client_error': (400, 499, 'yellow'),
    'server_error': (500, 599, 'red'),
}

# Supported timestamp formats
TIMESTAMP_FORMATS = [
    '%Y-%m-%dT%H:%M:%S.%fZ',
    '%Y-%m-%dT%H:%M:%SZ',
    '%Y-%m-%d %H:%M:%S.%f',
    '%Y-%m-%d %H:%M:%S',
    '%Y-%m-%dT%H:%M:%S%z',
    '%Y-%m-%dT%H:%M:%S.%f%z',
]

# Regex patterns for log parsing
PATTERNS = {
    'timestamp': r'(\d{4}-\d{2}-\d{2}[T\s]\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:?\d{2})?)',
    'log_level': r'\b(DEBUG|INFO|WARN|WARNING|ERROR|FATAL|CRITICAL)\b',
    'http_method': r'\b(GET|POST|PUT|DELETE|PATCH|HEAD|OPTIONS)\s+([^\s]+)',
    'status_code': r'\b(status[:\s=]+)?([1-5]\d{2})\b',
    'response_time': r'(\d+(?:\.\d+)?)\s*(ms|milliseconds?|s|seconds?)',
}

# JSON field mappings
JSON_FIELD_MAPPINGS = {
    'timestamp': ['timestamp', 'time', '@timestamp'],
    'level': ['level', 'severity'],
    'method': ['method', 'http_method'],
    'endpoint': ['path', 'endpoint', 'url'],
    'status': ['status', 'status_code'],
    'response_time': ['response_time', 'duration'],
    'message': ['message', 'msg'],
}