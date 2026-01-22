"""
Log Entry Model
Represents a single API log entry with parsing capabilities
Enhanced to support Java/Spring application logs with Unicode

Supports:
- JSON logs
- Generic API logs
- Java / Spring Boot logs
- START / STOP lifecycle logs
- Unicode-safe parsing
"""

import json
import re
from datetime import datetime
from typing import Optional, Dict


class LogEntry:
    """Represents a single parsed log entry"""

    def __init__(self, raw_line: str, line_number: int):
        self.raw_line = raw_line.strip()
        self.line_number = line_number

        # Core fields (used by LogViewer / filters)
        self.timestamp: Optional[datetime] = None
        self.level: Optional[str] = None
        self.method: Optional[str] = None
        self.endpoint: Optional[str] = None
        self.status_code: Optional[int] = None
        self.response_time: Optional[float] = None
        self.message: str = raw_line

        # Extended fields (Java / Spring)
        self.thread: Optional[str] = None
        self.logger: Optional[str] = None
        self.service_name: Optional[str] = None
        self.controller_name: Optional[str] = None
        self.operation_type: Optional[str] = None  # START / STOP

        # JSON support
        self.json_data: Optional[Dict] = None

        self._parse()

    # ======================================================
    # Main parsing dispatcher
    # ======================================================
    def _parse(self):
        """Attempt parsing in safe priority order"""

        # 1️⃣ JSON (standalone or embedded)
        if '{' in self.raw_line and '}' in self.raw_line:
            if self._parse_json_embedded():
                return

        # 2️⃣ Java / Spring format
        if self._parse_java_format(self.raw_line):
            return

        # 3️⃣ Generic / API logs
        self._parse_common_format()

    # ======================================================
    # JSON parsing
    # ======================================================
    def _parse_json_embedded(self) -> bool:
        try:
            start = self.raw_line.index('{')
            json_str = self.raw_line[start:]
            self.json_data = json.loads(json_str)
            self._extract_from_json()

            # Parse prefix before JSON if exists
            prefix = self.raw_line[:start]
            self._parse_java_format(prefix)

            return True
        except Exception:
            return False

    def _extract_from_json(self):
        data = self.json_data
        if not data:
            return

        self.timestamp = self._parse_timestamp(
            data.get('timestamp') or data.get('time') or data.get('@timestamp')
        )

        self.level = self.level or data.get('level') or data.get('severity')
        self.method = self.method or data.get('method') or data.get('http_method')
        self.endpoint = self.endpoint or data.get('path') or data.get('endpoint') or data.get('url')
        self.status_code = self.status_code or data.get('status') or data.get('status_code')
        self.response_time = data.get('response_time') or data.get('duration')

        json_msg = data.get('message') or data.get('msg')
        if json_msg:
            # Ensure message is always a string
            self.message = str(json_msg) if not isinstance(json_msg, str) else json_msg
        elif self.message == self.raw_line:
            self.message = ""

        # if self.message == self.raw_line:
        #     self.message = data.get('message') or data.get('msg') or str(data)[:120]

    # ======================================================
    # Java / Spring parsing
    # ======================================================
    def _parse_java_format(self, line: str) -> bool:
        pattern = (
            r'^(\d{2}:\d{2}:\d{2}\.\d{3})\s+'
            r'\[([^\]]+)\]\s+'
            r'(DEBUG|INFO|WARN|WARNING|ERROR|FATAL|CRITICAL)\s+'
            r'([^\s:]+)\s*::\s*(.+)$'
        )

        match = re.match(pattern, line, re.IGNORECASE)
        if not match:
            return False

        time_str, thread, level, logger, message = match.groups()

        try:
            today = datetime.now().date()
            self.timestamp = datetime.combine(
                today,
                datetime.strptime(time_str, '%H:%M:%S.%f').time()
            )
        except ValueError:
            pass

        self.thread = thread
        self.level = level.upper()
        self.logger = logger

        self._extract_message_details(message)
        return True

    def _extract_message_details(self, message: str):
        self.message = message

        # Controller / service
        ctrl_pattern = r'([A-Za-z]+(?:Cntr|Controller|Service)):\s*([A-Z0-9]+)'
        m = re.search(ctrl_pattern, message)
        if m:
            self.controller_name = m.group(1)
            self.endpoint = '/' + m.group(2)
            self.service_name = self.controller_name

        # START / STOP
        lifecycle = r'=+\s*/([A-Z0-9]+)\s+(START|STOP)'
        m = re.search(lifecycle, message)
        if m:
            self.endpoint = '/' + m.group(1)
            self.operation_type = m.group(2)

        # Standalone endpoint
        if not self.endpoint:
            m = re.search(r'/([A-Z0-9]+)', message)
            if m:
                self.endpoint = '/' + m.group(1)

        # HTTP method
        m = re.search(r'\b(GET|POST|PUT|DELETE|PATCH|HEAD|OPTIONS)\b', message)
        if m:
            self.method = m.group(1)

        if not self.method and self.endpoint:
            self.method = 'POST'

        # Status code
        status_patterns = [
            r'Response Code\s*:\s*(\d{3})',
            r'status[:\s=]+(\d{3})',
            r'RSLT_CD\[(\d+)\]'
        ]
        for p in status_patterns:
            m = re.search(p, message)
            if m:
                code = int(m.group(1))
                self.status_code = 404 if code == 719 else code
                break

        # Response time
        m = re.search(r'(\d+(?:\.\d+)?)\s*(ms|milliseconds?)', message)
        if m:
            self.response_time = float(m.group(1))

        # Normalize message
        if self.operation_type and self.endpoint:
            self.message = f"{self.operation_type} - {self.endpoint}"

    # ======================================================
    # Generic API log parsing (v1)
    # ======================================================
    def _parse_common_format(self):
        # Timestamp
        ts_patterns = [
            r'(\d{4}-\d{2}-\d{2}[T\s]\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:?\d{2})?)',
            r'(\d{2}:\d{2}:\d{2}(?:\.\d+)?)',
        ]
        for p in ts_patterns:
            m = re.search(p, self.raw_line)
            if m:
                self.timestamp = self._parse_timestamp(m.group(1))
                break

        # Level
        m = re.search(r'\b(DEBUG|INFO|WARN|WARNING|ERROR|FATAL|CRITICAL)\b', self.raw_line, re.I)
        if m:
            self.level = m.group(1).upper()

        # HTTP
        m = re.search(r'\b(GET|POST|PUT|DELETE|PATCH|HEAD|OPTIONS)\s+([^\s]+)', self.raw_line)
        if m:
            self.method, self.endpoint = m.groups()

        # Status
        m = re.search(r'\b([1-5]\d{2})\b', self.raw_line)
        if m:
            self.status_code = int(m.group(1))

        # Response time
        m = re.search(r'(\d+(?:\.\d+)?)\s*(ms|s)', self.raw_line)
        if m:
            value = float(m.group(1))
            self.response_time = value if m.group(2) == 'ms' else value * 1000

        # Extract trailing free-text message (after status / time)
        trailing_pattern = (
            r'\b(?:GET|POST|PUT|DELETE|PATCH|HEAD|OPTIONS)\s+'
            r'\S+\s+'  # endpoint
            r'(?:status=)?[1-5]\d{2}'  # status
            r'(?:\s+\d+(?:\.\d+)?(?:ms|s))?'  # optional time
            r'\s+(.*)$'  # message
        )

        m = re.search(trailing_pattern, self.raw_line, re.IGNORECASE)
        if m:
            self.message = m.group(1).strip()

    # ======================================================
    # Helpers
    # ======================================================
    def _parse_timestamp(self, ts: Optional[str]) -> Optional[datetime]:
        if not ts:
            return None

        formats = [
            '%Y-%m-%dT%H:%M:%S.%fZ',
            '%Y-%m-%dT%H:%M:%SZ',
            '%Y-%m-%d %H:%M:%S.%f',
            '%Y-%m-%d %H:%M:%S',
            '%Y-%m-%dT%H:%M:%S%z',
            '%Y-%m-%dT%H:%M:%S.%f%z',
            '%H:%M:%S.%f',
            '%H:%M:%S',
        ]

        for fmt in formats:
            try:
                parsed = datetime.strptime(ts, fmt)
                if fmt.startswith('%H'):
                    parsed = datetime.combine(datetime.now().date(), parsed.time())
                return parsed
            except ValueError:
                continue

        return None

    # ======================================================
    # UI helpers (unchanged – used by viewer)
    # ======================================================
    def get_level_color(self) -> str:
        return {
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARN': 'yellow',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'FATAL': 'bright_red',
            'CRITICAL': 'bright_red',
        }.get(self.level or '', 'white')

    def get_status_color(self) -> str:
        if not self.status_code:
            return 'white'
        if 200 <= self.status_code < 300:
            return 'green'
        if 300 <= self.status_code < 400:
            return 'blue'
        if 400 <= self.status_code < 500:
            return 'yellow'
        return 'red'

    def get_display_message(self, max_length: int = 60) -> str:
        """
        Return a cleaned, user-friendly message for table display.
        Fully compatible with v2 behavior.
        """
        # Ensure message is always a string
        if isinstance(self.message, dict):
            msg = str(self.message)
        else:
            msg = self.message or ""

        # Remove noisy prefixes
        prefixes_to_remove = [
            '===========',
            '===(',
        ]
        for prefix in prefixes_to_remove:
            if msg.startswith(prefix):
                msg = msg[len(prefix):].strip()

        # START / STOP override (highest priority)
        if self.operation_type:
            if self.endpoint:
                msg = f"{self.operation_type} - {self.endpoint}"
            else:
                msg = f"{self.operation_type} - operation"

        # RSLT_MSG cleanup
        rslt_msg = re.search(r'RSLT_MSG\[([^\]]+)\]', msg)
        if rslt_msg:
            msg = rslt_msg.group(1)

        # Remove excessive '='
        msg = re.sub(r'=+', '', msg).strip()

        # Remove noisy response-log markers
        msg = re.sub(r'\(.*?response log.*?\)', '', msg).strip()

        # Truncate safely
        if len(msg) > max_length:
            return msg[:max_length - 3] + "..."

        return msg