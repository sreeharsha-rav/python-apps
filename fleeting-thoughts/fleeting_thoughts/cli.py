"""Command Line Interface for Fleeting Thoughts.

This module provides the CLI commands for interacting with the application,
including adding and listing thoughts.
"""

import click
from datetime import datetime
from rich.console import Console
from rich.table import Table
from pathlib import Path

from .manager import ThoughtsManager

console = Console()
manager = ThoughtsManager(storage_dir="entries")

@click.group()
def cli():
    """Manage your fleeting thoughts with ease."""
    Path("entries").mkdir(exist_ok=True)

@cli.command()
@click.argument('content')
def add(content: str):
    """Add a new thought.

    Args:
        content (str): The content of the thought to add
    """
    try:
        thought = manager.add_thought(content)
        console.print(f"✓ Thought added at [green]{thought.timestamp}[/]")
    except Exception as e:
        console.print(f"[red]Error adding thought: {str(e)}[/]")

@cli.command()
@click.option('--date', default=None, help='Date in YYYY-MM-DD format. Defaults to today.')
def list(date: str | None):
    """List thoughts for a specific date.

    Args:
        date (str, optional): Date to list thoughts for. Defaults to today.
    """
    if date is None:
        date = datetime.now().date().isoformat()
    
    try:
        daily_thoughts = manager.get_thoughts_for_date(date)
        
        if not daily_thoughts or not daily_thoughts.thoughts:
            console.print(f"No thoughts found for [yellow]{date}[/]")
            return

        table = Table(show_header=True)
        table.add_column("Time", style="cyan")
        table.add_column("Thought", style="white")

        for thought in daily_thoughts.thoughts:
            time = thought.timestamp.strftime("%H:%M:%S")
            table.add_row(time, thought.content)

        console.print(f"\nThoughts for [yellow]{date}[/]:")
        console.print(table)
    except Exception as e:
        console.print(f"[red]Error listing thoughts: {str(e)}[/]")

@cli.command()
def list_all():
    """List all thoughts from all dates."""
    try:
        all_thoughts = manager.get_all_thoughts()
        
        if not all_thoughts:
            console.print("No thoughts found")
            return

        table = Table(show_header=True)
        table.add_column("Date", style="cyan")
        table.add_column("Time", style="cyan")
        table.add_column("Thought", style="white")

        for daily in sorted(all_thoughts, key=lambda x: x.date):
            for thought in daily.thoughts:
                date = daily.date
                time = thought.timestamp.strftime("%H:%M:%S")
                table.add_row(date, time, thought.content)

        console.print("\nAll thoughts:")
        console.print(table)
    except Exception as e:
        console.print(f"[red]Error listing thoughts: {str(e)}[/]")

if __name__ == '__main__':
    cli()
