import click
from datetime import date, datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from main.modules.thoughts.model import Thought
from main.modules.thoughts.service import ThoughtsService
from main.storage.json_file_manager import JSONFileManager

console = Console()
file_manager = JSONFileManager("./data")
service = ThoughtsService(file_manager)

@click.group()
def thoughts():
    """Manage your fleeting thoughts."""
    pass

@thoughts.command()
@click.option('--date', '-d', type=click.DateTime(formats=["%Y-%m-%d"]), 
              default=str(date.today()), help="Date for the thought (YYYY-MM-DD)")
@click.option('--content', '-c', prompt="Enter your thought", help="Content of your thought")
def add(date: datetime, content: str):
    """Add a new thought for the specified date."""
    # Convert datetime to date
    entry_date = date.date()
    
    # Create thought with current timestamp
    thought = Thought(content=content, timestamp=datetime.now())
    
    try:
        service.add_thought(thought, entry_date)
        console.print(Panel.fit(
            f"[bold green]Thought added successfully![/]\n\n[italic]{content}[/]", 
            title=f"Thought for {entry_date}",
            border_style="green"
        ))
    except Exception as e:
        console.print(f"[bold red]Error:[/] {str(e)}")

@thoughts.command()
@click.option('--date', '-d', type=click.DateTime(formats=["%Y-%m-%d"]), 
              default=str(date.today()), help="Date to view thoughts from (YYYY-MM-DD)")
def list(date: datetime):
    """List thoughts for a specific date."""
    # Convert datetime to date
    entry_date = date.date()
    
    try:
        thoughts = service.get_thoughts(entry_date)
        
        if not thoughts.thoughts:
            console.print(f"[yellow]No thoughts found for {entry_date}[/]")
            return
        
        table = Table(title=f"Thoughts for {entry_date}")
        table.add_column("ID", style="dim", width=4)
        table.add_column("Content", style="green")
        table.add_column("Time", style="blue")
        
        for i, thought in enumerate(thoughts.thoughts):
            created_at = thought.timestamp.strftime("%H:%M:%S") if thought.timestamp else "N/A"
            table.add_row(str(i+1), thought.content, created_at)
        
        console.print(table)
    except Exception as e:
        console.print(f"[bold red]Error:[/] {str(e)}")

@thoughts.command()
@click.option('--date', '-d', type=click.DateTime(formats=["%Y-%m-%d"]), 
              default=str(date.today()), help="Date to modify thoughts from (YYYY-MM-DD)")
@click.option('--id', '-i', type=int, prompt="Thought ID to edit", help="ID of the thought to edit")
@click.option('--content', '-c', prompt="New content", help="New content for the thought")
def edit(date: datetime, id: int, content: str):
    """Edit an existing thought."""
    # Convert datetime to date
    entry_date = date.date()
    
    try:
        thoughts = service.get_thoughts(entry_date)
        
        if not thoughts.thoughts or id > len(thoughts.thoughts) or id <= 0:
            console.print(f"[bold red]Error:[/] Invalid thought ID. Thought with ID {id} not found.")
            return
        
        # Preserve timestamp when editing
        timestamp = thoughts.thoughts[id-1].timestamp
        thoughts.thoughts[id-1] = Thought(content=content, timestamp=timestamp)
        
        # Save updated thoughts
        service.save_thoughts(thoughts, entry_date)
        
        console.print(f"[bold green]Thought #{id} updated successfully![/]")
    except Exception as e:
        console.print(f"[bold red]Error:[/] {str(e)}")

@thoughts.command()
@click.option('--date', '-d', type=click.DateTime(formats=["%Y-%m-%d"]), 
              default=str(date.today()), help="Date to delete thought from (YYYY-MM-DD)")
@click.option('--id', '-i', type=int, prompt="Thought ID to delete", help="ID of the thought to delete")
@click.confirmation_option(prompt="Are you sure you want to delete this thought?")
def delete(date: datetime, id: int):
    """Delete a thought."""
    # Convert datetime to date
    entry_date = date.date()
    
    try:
        thoughts = service.get_thoughts(entry_date)
        
        if not thoughts.thoughts or id > len(thoughts.thoughts) or id <= 0:
            console.print(f"[bold red]Error:[/] Invalid thought ID. Thought with ID {id} not found.")
            return
        
        # Remove thought (adjust for zero-based indexing)
        del thoughts.thoughts[id-1]
        
        # Save updated thoughts
        service.save_thoughts(thoughts, entry_date)
        
        console.print(f"[bold green]Thought #{id} deleted successfully![/]")
    except Exception as e:
        console.print(f"[bold red]Error:[/] {str(e)}")