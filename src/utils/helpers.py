"""
Helper Functions
Utility functions for the log viewer
"""

from rich.console import Console
from rich.markdown import Markdown

console = Console()


def show_help():
    """Display help information"""
    help_text = """
# API Log Viewer Commands

## Viewing
- `summary` - Show log statistics summary
- `list [limit]` - List log entries (default: 50)
- `view <line_number>` - View detailed entry information
- `stats` - Alias for summary

## Filtering
- `filter level <LEVEL>` - Filter by log level (DEBUG, INFO, WARN, ERROR)
- `filter method <METHOD>` - Filter by HTTP method (GET, POST, etc.)
- `filter status <CODE>` - Filter by status code (200, 404, etc.)
- `filter thread <NAME>` - Filter by thread name (e.g., http-nio, SimpleAsyncTaskExecutor)
- `filter service <NAME>` - Filter by service/controller name
- `filter search <TEXT>` - Search for text in logs (supports Unicode)
- `clear` - Clear all filters

## Editing
- `edit <line_number>` - Edit a specific log entry
- `save [path]` - Save changes to file

## Export
- `export <path>` - Export filtered entries to new file

## Other
- `help` - Show this help message
- `quit` or `exit` - Exit the application

## Examples
```
› filter level ERROR          # Show only errors
› filter thread http-nio      # Show HTTP request threads
› filter service BackendInvoiceCntr  # Show specific service logs
› filter status 404           # Show 404 errors
› filter search Firebase      # Search for Firebase-related logs
```
"""
    console.print(Markdown(help_text))


def format_file_size(size_bytes: int) -> str:
    """Format file size in human-readable format"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"


def truncate_text(text: str, max_length: int) -> str:
    """Truncate text to max length with ellipsis"""
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."