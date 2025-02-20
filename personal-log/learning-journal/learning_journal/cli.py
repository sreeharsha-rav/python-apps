"""Command Line Interface for the Learning Journal.

This module provides the CLI commands for interacting with the application,
including adding and listing learning journal entries.
"""

from datetime import date
from pathlib import Path
import click
from rich.console import Console
from rich.table import Table
from .storage import JsonStorage
from .manager import JournalManager

console = Console()

@click.group()
@click.pass_context
def cli(ctx):
    """Learning Journal - Track your daily learnings"""
    storage = JsonStorage()
    ctx.obj = JournalManager(storage)
    Path("entries").mkdir(exist_ok=True)

@cli.command()
@click.option('--date_str', '-d', default=str(date.today()),
              help='Entry date (YYYY-MM-DD)')
@click.pass_obj
def add(manager: JournalManager, date_str: str):  # Renamed parameter to avoid shadowing
    """Add a new learning entry"""
    try:
        entry_date = date.fromisoformat(date_str)
        manager.add_entry(entry_date)
        console.print(f"[green]Entry added for {date_str}[/green]")
    except ValueError as e:
        console.print(f"[red]Error: {e}[/red]")

@cli.command()
@click.option('--date_str', '-d', default=str(date.today()),
              help='Entry date (YYYY-MM-DD)')
@click.pass_obj
def show(manager: JournalManager, date_str: str):
    """Show learning entries for a date"""
    try:
        entry_date = date.fromisoformat(date_str)
        entry = manager.get_entry(entry_date)
        
        if not entry:
            console.print(f"[yellow]No entries found for {date_str}[/yellow]")
            return
        
        table = Table(title=f"Learnings for {date_str}")
        table.add_column("Topic", style="cyan")
        table.add_column("Insight", style="green")
        table.add_column("Connection", style="blue")
        
        for learning in entry.learnings:
            table.add_row(
                learning.topic,
                learning.insight,
                learning.connection or "-"
            )
        
        console.print(table)
    except ValueError as e:
        console.print(f"[red]Error: {e}[/red]")