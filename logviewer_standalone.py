#!/usr/bin/env python3
"""
API Log Viewer - Standalone Single File Application
Based on refactored code structure
Can be run directly or accept drag & drop file

Features:
- Full Java/Spring log support
- Unicode text handling
- Drag & drop functionality
- All filtering and viewing features
"""

import json
import re
import sys
import os
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.syntax import Syntax
    from rich.text import Text
    from rich.progress import track
    from rich.prompt import Prompt, Confirm
    from rich.markdown import Markdown
    from rich import box
except ImportError:
    print("ERROR: Required library 'rich' is not installed.")
    print("Please install it using: pip install rich")
    sys.exit(1)

console = Console()


# ============================================================================
# LogEntry Class - Refactored Version
# ============================================================================

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

        # Extract trailing free-text message
        trailing_pattern = (
            r'\b(?:GET|POST|PUT|DELETE|PATCH|HEAD|OPTIONS)\s+'
            r'\S+\s+'
            r'(?:status=)?[1-5]\d{2}'
            r'(?:\s+\d+(?:\.\d+)?(?:ms|s))?'
            r'\s+(.*)$'
        )

        m = re.search(trailing_pattern, self.raw_line, re.IGNORECASE)
        if m:
            self.message = m.group(1).strip()

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
        """Return a cleaned, user-friendly message for table display"""
        # Ensure message is always a string
        if isinstance(self.message, dict):
            msg = str(self.message)
        else:
            msg = self.message or ""

        # Remove noisy prefixes
        prefixes_to_remove = ['===========', '===(']
        for prefix in prefixes_to_remove:
            if msg.startswith(prefix):
                msg = msg[len(prefix):].strip()

        # START / STOP override
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


# ============================================================================
# LogViewer Class - Refactored Version
# ============================================================================

class LogViewer:
    """Main log viewer application"""

    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self.entries: List[LogEntry] = []
        self.filtered_entries: List[LogEntry] = []
        self.current_filter: Dict[str, Any] = {}

        if not self.file_path.exists():
            console.print(f"[red]Error: File not found: {file_path}[/red]")
            sys.exit(1)

    def load(self):
        """Load and parse log file"""
        console.print(f"[cyan]Loading log file: {self.file_path}[/cyan]")

        try:
            with open(self.file_path, 'r', encoding='utf-8', errors='replace') as f:
                lines = f.readlines()

            for i, line in track(enumerate(lines, 1), description="Parsing logs...", total=len(lines)):
                if line.strip():
                    self.entries.append(LogEntry(line, i))

            self.filtered_entries = self.entries.copy()
            console.print(f"[green]✓ Loaded {len(self.entries)} log entries[/green]\n")

        except Exception as e:
            console.print(f"[red]Error loading file: {e}[/red]")
            sys.exit(1)

    def display_summary(self):
        """Display log statistics summary"""
        table = Table(title="Log Summary", box=box.ROUNDED)
        table.add_column("Metric", style="cyan", width=20)
        table.add_column("Value", style="green")

        levels = {}
        methods = {}
        status_codes = {}
        threads = {}
        services = {}

        for entry in self.filtered_entries:
            if entry.level:
                levels[entry.level] = levels.get(entry.level, 0) + 1
            if entry.method:
                methods[entry.method] = methods.get(entry.method, 0) + 1
            if entry.status_code:
                status_codes[entry.status_code] = status_codes.get(entry.status_code, 0) + 1
            if entry.thread:
                thread_name = entry.thread.split('-')[0]
                threads[thread_name] = threads.get(thread_name, 0) + 1
            if entry.service_name:
                services[entry.service_name] = services.get(entry.service_name, 0) + 1

        table.add_row("Total Entries", str(len(self.filtered_entries)))
        table.add_row("File Size", f"{self.file_path.stat().st_size / 1024:.2f} KB")

        if levels:
            top_levels = sorted(levels.items(), key=lambda x: x[1], reverse=True)[:5]
            table.add_row("Log Levels", ", ".join(f"{k}: {v}" for k, v in top_levels))

        if methods:
            table.add_row("HTTP Methods", ", ".join(f"{k}: {v}" for k, v in sorted(methods.items())))

        if status_codes:
            top_codes = sorted(status_codes.items(), key=lambda x: x[1], reverse=True)[:5]
            table.add_row("Status Codes", ", ".join(f"{k}: {v}" for k, v in top_codes))

        if threads:
            top_threads = sorted(threads.items(), key=lambda x: x[1], reverse=True)[:5]
            table.add_row("Top Threads", ", ".join(f"{k}: {v}" for k, v in top_threads))

        if services:
            top_services = sorted(services.items(), key=lambda x: x[1], reverse=True)[:5]
            table.add_row("Top Services", ", ".join(f"{k}: {v}" for k, v in top_services))

        console.print(table)
        console.print()

    def display_entries(self, limit: int = 50):
        """Display log entries in a table"""
        table = Table(
            title=f"Log Entries (showing {min(limit, len(self.filtered_entries))} of {len(self.filtered_entries)})",
            box=box.SIMPLE,
            show_lines=False
        )

        table.add_column("#", style="dim", width=6)
        table.add_column("Time", style="cyan", width=12)
        table.add_column("Level", width=7)
        table.add_column("Thread", style="blue", width=25, overflow="fold")
        table.add_column("Service", style="magenta", width=20, overflow="fold")
        table.add_column("Method", style="blue", width=6)
        table.add_column("Endpoint", style="yellow", width=20, overflow="fold")
        table.add_column("Status", width=6)
        table.add_column("Message", width=35, overflow="fold")

        for entry in self.filtered_entries[:limit]:
            thread_display = (entry.thread[:22] + "...") if entry.thread and len(entry.thread) > 25 else (entry.thread or "-")
            service_display = (entry.service_name[:17] + "...") if entry.service_name and len(entry.service_name) > 20 else (entry.service_name or "-")
            endpoint_display = (entry.endpoint[:17] + "...") if entry.endpoint and len(entry.endpoint) > 20 else (entry.endpoint or "-")

            msg_text = entry.get_display_message(35) or "-"

            # Message coloring based on level
            if entry.level in ("ERROR", "FATAL", "CRITICAL"):
                msg_style = "red"
            elif entry.level in ("WARN", "WARNING"):
                msg_style = "yellow"
            elif entry.level == "DEBUG":
                msg_style = "dim"
            else:
                msg_style = "white"

            table.add_row(
                str(entry.line_number),
                entry.timestamp.strftime("%H:%M:%S.%f")[:-3] if entry.timestamp else "-",
                Text(entry.level or "-", style=entry.get_level_color()),
                thread_display,
                service_display,
                entry.method or "-",
                endpoint_display,
                Text(str(entry.status_code) if entry.status_code else "-", style=entry.get_status_color()),
                Text(msg_text, style=msg_style)
            )

        console.print(table)
        console.print()

    def view_entry_detail(self, line_number: int):
        """View detailed information about a specific entry"""
        entry = next((e for e in self.entries if e.line_number == line_number), None)

        if not entry:
            console.print(f"[red]Entry #{line_number} not found[/red]")
            return

        panel_content = f"""[cyan]Line Number:[/cyan] {entry.line_number}
[cyan]Timestamp:[/cyan] {entry.timestamp or 'N/A'}
[cyan]Level:[/cyan] [{entry.get_level_color()}]{entry.level or 'N/A'}[/{entry.get_level_color()}]
[cyan]Thread:[/cyan] {entry.thread or 'N/A'}
[cyan]Logger:[/cyan] {entry.logger or 'N/A'}
[cyan]Service:[/cyan] {entry.service_name or 'N/A'}
[cyan]Method:[/cyan] {entry.method or 'N/A'}
[cyan]Endpoint:[/cyan] {entry.endpoint or 'N/A'}
[cyan]Status:[/cyan] [{entry.get_status_color()}]{entry.status_code or 'N/A'}[/{entry.get_status_color()}]

[cyan]Message:[/cyan] {entry.message}"""

        console.print(Panel(panel_content, title=f"Entry #{line_number}", border_style="blue"))

        if entry.json_data:
            syntax = Syntax(json.dumps(entry.json_data, indent=2, ensure_ascii=False), "json", theme="monokai")
            console.print(Panel(syntax, title="JSON Data", border_style="green"))

        console.print(Panel(entry.raw_line, title="Raw Line", border_style="green"))
        console.print()

    def filter_logs(self, level=None, method=None, status_code=None, search=None, thread=None, service=None):
        """Filter log entries"""
        self.filtered_entries = self.entries.copy()
        self.current_filter = {}

        if level:
            self.filtered_entries = [e for e in self.filtered_entries if e.level and e.level.upper() == level.upper()]
            self.current_filter['level'] = level

        if method:
            self.filtered_entries = [e for e in self.filtered_entries if e.method and e.method.upper() == method.upper()]
            self.current_filter['method'] = method

        if status_code:
            self.filtered_entries = [e for e in self.filtered_entries if e.status_code == status_code]
            self.current_filter['status_code'] = status_code

        if thread:
            self.filtered_entries = [e for e in self.filtered_entries if e.thread and thread.lower() in e.thread.lower()]
            self.current_filter['thread'] = thread

        if service:
            self.filtered_entries = [e for e in self.filtered_entries if e.service_name and service.lower() in e.service_name.lower()]
            self.current_filter['service'] = service

        if search:
            self.filtered_entries = [e for e in self.filtered_entries if search.lower() in e.raw_line.lower()]
            self.current_filter['search'] = search

        filter_msg = " | ".join(f"{k}={v}" for k, v in self.current_filter.items())
        console.print(f"[green]✓ Filtered to {len(self.filtered_entries)} entries[/green]" +
                     (f" [dim]({filter_msg})[/dim]" if filter_msg else ""))
        console.print()

    def clear_filters(self):
        """Clear all filters"""
        self.filtered_entries = self.entries.copy()
        self.current_filter = {}
        console.print("[green]✓ Filters cleared[/green]\n")

    def export_filtered(self, output_path: str):
        """Export filtered entries to a new file"""
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                for entry in self.filtered_entries:
                    f.write(entry.raw_line + '\n')

            console.print(f"[green]✓ Exported {len(self.filtered_entries)} entries to {output_path}[/green]\n")
        except Exception as e:
            console.print(f"[red]Error exporting: {e}[/red]\n")

    def save(self, output_path: Optional[str] = None):
        """Save modified logs to file"""
        save_path = output_path or self.file_path

        try:
            with open(save_path, 'w', encoding='utf-8') as f:
                for entry in sorted(self.entries, key=lambda e: e.line_number):
                    f.write(entry.raw_line + '\n')

            console.print(f"[green]✓ Saved to {save_path}[/green]\n")
        except Exception as e:
            console.print(f"[red]Error saving: {e}[/red]\n")


# ============================================================================
# Helper Functions
# ============================================================================

def show_help():
    """Display help information"""
    help_text = """
# API Log Viewer Commands

**Viewing:** summary | list [limit] | view <line> | stats
**Filtering:** filter level/method/status/thread/service/search <value> | clear
**Export:** export <path>
**Other:** help | quit/exit

**Examples:**
  › filter level ERROR
  › filter thread http-nio
  › filter service BackendInvoiceCntr
  › filter search DATA NOT FOUND
  › export errors.log
"""
    console.print(Markdown(help_text))


# ============================================================================
# Main Application
# ============================================================================

def main():
    """Main application entry point"""

    # Check if file was drag-and-dropped or passed as argument
    if len(sys.argv) < 2:
        console.print(Panel.fit(
            "[bold yellow]API Log Viewer[/bold yellow]\n\n" +
            "[dim]Drag & drop a log file onto this application\n" +
            "Or run: python logviewer_standalone.py <logfile>[/dim]\n\n" +
            "[cyan]Waiting for file path...[/cyan]",
            border_style="yellow"
        ))

        file_path = input("\nEnter log file path: ").strip().strip('"\'')
        if not file_path:
            console.print("[red]No file provided. Exiting.[/red]")
            sys.exit(1)
    else:
        file_path = sys.argv[1].strip().strip('"\'')

    # Display banner
    console.print(Panel.fit(
        "[bold cyan]API Log Viewer[/bold cyan]\n" +
        "[dim]Enhanced for Java/Spring logs with Unicode support[/dim]",
        border_style="cyan"
    ))
    console.print()

    viewer = LogViewer(file_path)
    viewer.load()
    viewer.display_summary()

    console.print("[dim]Type 'help' for commands | 'quit' to exit[/dim]\n")

    # Interactive command loop
    while True:
        try:
            command = Prompt.ask("[bold green]›[/bold green]").strip()

            if not command:
                continue

            parts = command.split()
            cmd = parts[0].lower()

            if cmd in ['quit', 'exit', 'q']:
                if Confirm.ask("Save changes before exiting?", default=False):
                    viewer.save()
                console.print("[cyan]Goodbye![/cyan]")
                break

            elif cmd == 'help':
                show_help()

            elif cmd in ['summary', 'stats']:
                viewer.display_summary()

            elif cmd == 'list':
                limit = int(parts[1]) if len(parts) > 1 else 50
                viewer.display_entries(limit)

            elif cmd == 'view':
                if len(parts) >= 2:
                    viewer.view_entry_detail(int(parts[1]))
                else:
                    console.print("[red]Usage: view <line_number>[/red]\n")

            elif cmd == 'filter':
                if len(parts) >= 3:
                    filter_type = parts[1].lower()
                    value = ' '.join(parts[2:])

                    if filter_type == 'level':
                        viewer.filter_logs(level=value)
                    elif filter_type == 'method':
                        viewer.filter_logs(method=value)
                    elif filter_type == 'status':
                        viewer.filter_logs(status_code=int(value))
                    elif filter_type == 'thread':
                        viewer.filter_logs(thread=value)
                    elif filter_type == 'service':
                        viewer.filter_logs(service=value)
                    elif filter_type == 'search':
                        viewer.filter_logs(search=value)
                    else:
                        console.print("[red]Unknown filter type[/red]\n")

                    viewer.display_entries()
                else:
                    console.print("[red]Usage: filter <type> <value>[/red]\n")

            elif cmd == 'clear':
                viewer.clear_filters()
                viewer.display_entries()

            elif cmd == 'export':
                if len(parts) >= 2:
                    viewer.export_filtered(parts[1])
                else:
                    console.print("[red]Usage: export <output_path>[/red]\n")

            else:
                console.print(f"[red]Unknown command: {cmd}[/red]\n")

        except KeyboardInterrupt:
            console.print("\n[yellow]Use 'quit' to exit[/yellow]\n")
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]\n")


if __name__ == '__main__':
    main()