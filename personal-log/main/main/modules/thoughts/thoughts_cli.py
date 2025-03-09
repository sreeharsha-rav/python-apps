import click
from datetime import date, datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich import box
from rich.spinner import Spinner
from rich.live import Live

from main.modules.thoughts.model import Thought
from main.modules.thoughts.service import ThoughtsService
from main.storage.json_file_manager import JSONFileManager

console = Console()
file_manager = JSONFileManager("./data")
service = ThoughtsService(file_manager)

@click.group()
def thoughts():
    """✨ Capture and manage your fleeting thoughts."""
    pass

@thoughts.command()
@click.option('--date', '-d', type=click.DateTime(formats=["%Y-%m-%d"]), 
              default=str(date.today()), help="Date for the thought (YYYY-MM-DD)")
@click.option('--content', '-c', prompt="💭 Enter your thought", help="Content of your thought")
def add(date: datetime, content: str):
    """📝 Add a new thought for the specified date."""
    # Convert datetime to date
    entry_date = date.date()
    
    with console.status("[bold green]Saving your thought...", spinner="dots"):
        # Create thought with current timestamp
        thought = Thought(content=content, timestamp=datetime.now())
        
        try:
            service.add_thought(thought, entry_date)
            console.print(Panel.fit(
                f"[bold green]Thought added successfully![/]\n\n[italic]{content}[/]", 
                title=f"💭 Thought for {entry_date}",
                border_style="green",
                box=box.ROUNDED
            ))
        except Exception as e:
            console.print(f"[bold red]❌ Error:[/] {str(e)}")

@thoughts.command()
@click.option('--date', '-d', type=click.DateTime(formats=["%Y-%m-%d"]), 
              default=str(date.today()), help="Date to view thoughts from (YYYY-MM-DD)")
def list(date: datetime):
    """📋 List thoughts for a specific date."""
    # Convert datetime to date
    entry_date = date.date()
    
    with console.status(f"[bold blue]Loading thoughts for {entry_date}...", spinner="dots"):
        try:
            thoughts = service.get_thoughts(entry_date)
            
            if not thoughts.thoughts:
                console.print(f"[yellow]📭 No thoughts found for {entry_date}[/]")
                return
            
            table = Table(
                title=f"💭 Thoughts for {entry_date}",
                box=box.ROUNDED,
                highlight=True,
                border_style="bright_blue"
            )
            table.add_column("#", style="dim cyan", width=4)
            table.add_column("✏️ Thought", style="green")
            table.add_column("⏰ Time", style="blue")
            
            for i, thought in enumerate(thoughts.thoughts):
                created_at = thought.timestamp.strftime("%H:%M:%S") if thought.timestamp else "N/A"
                table.add_row(str(i+1), thought.content, created_at)
            
            console.print("\n")
            console.print(table)
            console.print(f"\n[dim italic]Total: {len(thoughts.thoughts)} thoughts[/]")
        except Exception as e:
            console.print(f"[bold red]❌ Error:[/] {str(e)}")

@thoughts.command()
@click.option('--date', '-d', type=click.DateTime(formats=["%Y-%m-%d"]), 
              default=str(date.today()), help="Date to modify thoughts from (YYYY-MM-DD)")
@click.option('--id', '-i', type=int, prompt="🔍 Thought ID to edit", help="ID of the thought to edit")
@click.option('--content', '-c', prompt="✏️ New content", help="New content for the thought")
def edit(date: datetime, id: int, content: str):
    """✏️ Edit an existing thought."""
    # Convert datetime to date
    entry_date = date.date()
    
    with console.status("[bold yellow]Updating your thought...", spinner="line"):
        try:
            thoughts = service.get_thoughts(entry_date)
            
            if not thoughts.thoughts or id > len(thoughts.thoughts) or id <= 0:
                console.print(f"[bold red]❌ Error:[/] Invalid thought ID. Thought with ID {id} not found.")
                return
            
            # Show original thought
            original = thoughts.thoughts[id-1].content
            console.print(f"[dim]Original: [/][italic]{original}[/]")
            
            # Preserve timestamp when editing
            timestamp = thoughts.thoughts[id-1].timestamp
            thoughts.thoughts[id-1] = Thought(content=content, timestamp=timestamp)
            
            # Save updated thoughts
            service.save_thoughts(thoughts, entry_date)
            
            console.print(f"[bold green]✅ Thought #{id} updated successfully![/]")
        except Exception as e:
            console.print(f"[bold red]❌ Error:[/] {str(e)}")

@thoughts.command()
@click.option('--date', '-d', type=click.DateTime(formats=["%Y-%m-%d"]), 
              default=str(date.today()), help="Date to delete thought from (YYYY-MM-DD)")
@click.option('--id', '-i', type=int, prompt="🔍 Thought ID to delete", help="ID of the thought to delete")
@click.confirmation_option(prompt="❗ Are you sure you want to delete this thought?")
def delete(date: datetime, id: int):
    """🗑️ Delete a thought."""
    # Convert datetime to date
    entry_date = date.date()
    
    with console.status("[bold red]Deleting thought...", spinner="point"):
        try:
            thoughts = service.get_thoughts(entry_date)
            
            if not thoughts.thoughts or id > len(thoughts.thoughts) or id <= 0:
                console.print(f"[bold red]❌ Error:[/] Invalid thought ID. Thought with ID {id} not found.")
                return
            
            # Show thought being deleted
            to_delete = thoughts.thoughts[id-1].content
            console.print(f"[dim]Deleting: [/][italic]{to_delete}[/]")
            
            # Remove thought (adjust for zero-based indexing)
            del thoughts.thoughts[id-1]
            
            # Save updated thoughts
            service.save_thoughts(thoughts, entry_date)
            
            console.print(f"[bold green]✅ Thought #{id} deleted successfully![/]")
        except Exception as e:
            console.print(f"[bold red]❌ Error:[/] {str(e)}")