"""
Log Viewer Class
Main log viewer application logic with enhanced display
"""

import sys
import json
from pathlib import Path
from typing import Optional, List, Dict, Any

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.syntax import Syntax
from rich.text import Text
from rich.progress import track
from rich import box

from src.models.log_entry import LogEntry

console = Console()


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
            # Read with UTF-8 encoding for Unicode support
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

        # Count by level
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
                thread_name = entry.thread.split('-')[0]  # Group similar threads
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
            # Truncate long fields
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


            # table.add_row(
            #     str(entry.line_number),
            #     entry.timestamp.strftime("%H:%M:%S.%f")[:-3] if entry.timestamp else "-",
            #     Text(entry.level or "-", style=entry.get_level_color()),
            #     thread_display,
            #     service_display,
            #     entry.method or "-",
            #     endpoint_display,
            #     Text(str(entry.status_code) if entry.status_code else "-", style=entry.get_status_color()),
            #     entry.get_display_message(35)
            # )

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
[cyan]Status Code:[/cyan] [{entry.get_status_color()}]{entry.status_code or 'N/A'}[/{entry.get_status_color()}]
[cyan]Response Time:[/cyan] {entry.response_time or 'N/A'} ms

[cyan]Message:[/cyan]
{entry.message}
"""

        console.print(Panel(panel_content, title=f"Entry #{line_number}", border_style="blue"))

        if entry.json_data:
            syntax = Syntax(json.dumps(entry.json_data, indent=2, ensure_ascii=False), "json", theme="monokai")
            console.print(Panel(syntax, title="JSON Data", border_style="green"))

        console.print(Panel(entry.raw_line, title="Raw Line", border_style="green"))
        console.print()

    def filter_logs(self, level: Optional[str] = None, method: Optional[str] = None,
                    status_code: Optional[int] = None, search: Optional[str] = None,
                    thread: Optional[str] = None, service: Optional[str] = None):
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

    def edit_entry(self, line_number: int, new_content: str):
        """Edit a specific log entry"""
        entry = next((e for e in self.entries if e.line_number == line_number), None)

        if not entry:
            console.print(f"[red]Entry #{line_number} not found[/red]")
            return

        entry.raw_line = new_content
        entry._parse()
        console.print(f"[green]✓ Entry #{line_number} updated[/green]\n")

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