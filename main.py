#!/usr/bin/env python3
"""
API Log Viewer - Main Entry Point
A feature-rich tool for viewing and editing API logs
Enhanced for Java/Spring application logs with Unicode support
"""

import sys
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.markdown import Markdown

from src.log_viewer import LogViewer
from src.utils.helpers import show_help

console = Console()


def main():
    """Main application entry point"""
    if len(sys.argv) < 2:
        console.print("[yellow]Usage: python main.py <log_file_path>[/yellow]")
        console.print("[dim]Example: python main.py examples/sample_api_format.log[/dim]")
        sys.exit(1)

    # Display banner
    console.print(Panel.fit(
        "[bold cyan]API Log Viewer[/bold cyan]\n" +
        "[dim]Enhanced for Java/Spring logs with Unicode support[/dim]",
        border_style="cyan"
    ))
    console.print()

    viewer = LogViewer(sys.argv[1])
    viewer.load()
    viewer.display_summary()

    console.print("[dim]Type 'help' for available commands[/dim]\n")

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

            elif cmd == 'summary':
                viewer.display_summary()

            elif cmd == 'list':
                limit = int(parts[1]) if len(parts) > 1 else 50
                viewer.display_entries(limit)

            elif cmd == 'view':
                if len(parts) < 2:
                    console.print("[red]Usage: view <line_number>[/red]\n")
                else:
                    viewer.view_entry_detail(int(parts[1]))

            elif cmd == 'filter':
                if len(parts) < 3:
                    console.print("[red]Usage: filter <level|method|status|thread|service|search> <value>[/red]\n")
                else:
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
                        console.print(
                            "[red]Unknown filter type. Use: level, method, status, thread, service, or search[/red]\n")

                    viewer.display_entries()

            elif cmd == 'clear':
                viewer.clear_filters()
                viewer.display_entries()

            elif cmd == 'edit':
                if len(parts) < 2:
                    console.print("[red]Usage: edit <line_number>[/red]\n")
                else:
                    line_num = int(parts[1])
                    viewer.view_entry_detail(line_num)
                    new_content = Prompt.ask("Enter new content")
                    viewer.edit_entry(line_num, new_content)

            elif cmd == 'save':
                output_path = parts[1] if len(parts) > 1 else None
                viewer.save(output_path)

            elif cmd == 'export':
                if len(parts) < 2:
                    console.print("[red]Usage: export <output_path>[/red]\n")
                else:
                    viewer.export_filtered(parts[1])

            elif cmd == 'stats':
                # Additional statistics command
                viewer.display_summary()

            else:
                console.print(f"[red]Unknown command: {cmd}[/red]")
                console.print("[dim]Type 'help' for available commands[/dim]\n")

        except KeyboardInterrupt:
            console.print("\n[yellow]Use 'quit' or 'exit' to leave[/yellow]\n")
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]\n")


if __name__ == '__main__':
    main()