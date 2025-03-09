import click
from datetime import date, datetime
from typing import Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich import box
from rich.spinner import Spinner
from rich.markdown import Markdown

from main.modules.learnings.model import Learning, LearningEntry
from main.modules.learnings.service import LearningsService
from main.storage.json_file_manager import JSONFileManager

console = Console()
file_manager = JSONFileManager("./data")
service = LearningsService(file_manager)

@click.group()
def learnings():
    """📚 Document and manage your learning journey."""
    pass

@learnings.command()
@click.option('--date', '-d', type=click.DateTime(formats=["%Y-%m-%d"]), 
              default=str(date.today()), help="Date for the learning (YYYY-MM-DD)")
@click.option('--topic', '-t', prompt="📌 Topic", help="Topic or context of the learning")
@click.option('--insight', '-i', prompt="💡 Insight", help="What you learned")
@click.option('--connection', '-c', prompt="🔄 Connection (optional)", help="How this connects to previous learnings", default="")
def add(date: datetime, topic: str, insight: str, connection: Optional[str] = None):
    """📝 Add a new learning entry."""
    entry_date = date.date()
    
    with console.status("[bold green]Recording your learning...", spinner="dots"):
        # Create learning
        learning = Learning(
            topic=topic,
            insight=insight,
            connection=connection
        )
        
        try:
            service.add_learning(learning, entry_date)
            console.print(Panel.fit(
                f"[bold]📌 Topic:[/] {topic}\n[bold]💡 Insight:[/] {insight}" + 
                (f"\n[bold]🔄 Connection:[/] {connection}" if connection else ""),
                title="✨ Learning Added Successfully",
                border_style="green",
                box=box.ROUNDED
            ))
        except Exception as e:
            console.print(f"[bold red]❌ Error:[/] {str(e)}")

@learnings.command()
@click.option('--date', '-d', type=click.DateTime(formats=["%Y-%m-%d"]), 
              default=str(date.today()), help="Date to view learnings from (YYYY-MM-DD)")
def list(date: datetime):
    """📋 List learning entries for a specific date."""
    entry_date = date.date()
    
    with console.status(f"[bold blue]Loading learnings for {entry_date}...", spinner="dots"):
        try:
            learning_entry = service.get_learnings(entry_date)
            
            if not learning_entry.learnings:
                console.print(f"[yellow]📭 No learning entries found for {entry_date}[/]")
                return
            
            console.print(f"[bold green]📚 Learning entries for {entry_date}:[/]\n")
            
            for i, learning in enumerate(learning_entry.learnings, 1):
                panel_content = f"[bold]📌 Topic:[/] {learning.topic}\n[bold]💡 Insight:[/] {learning.insight}"
                if learning.connection:
                    panel_content += f"\n[bold]🔄 Connection:[/] {learning.connection}"
                    
                console.print(Panel.fit(
                    panel_content,
                    title=f"Learning #{i}",
                    border_style="blue",
                    box=box.ROUNDED
                ))
                
                if i < len(learning_entry.learnings):
                    console.print("")  # Add spacing between entries
                    
            console.print(f"\n[dim italic]Total: {len(learning_entry.learnings)} learning entries[/]")
                    
        except Exception as e:
            console.print(f"[bold red]❌ Error:[/] {str(e)}")

@learnings.command()
@click.option('--date', '-d', type=click.DateTime(formats=["%Y-%m-%d"]), 
              default=str(date.today()), help="Date to modify learning from (YYYY-MM-DD)")
@click.option('--id', '-i', type=int, prompt="🔍 Learning ID to edit", help="ID of the learning to edit")
@click.option('--topic', '-t', help="Updated topic")
@click.option('--insight', '-n', help="Updated insight")
@click.option('--connection', '-c', help="Updated connection")
def edit(date: datetime, id: int, topic: Optional[str], insight: Optional[str], connection: Optional[str]):
    """✏️ Edit an existing learning entry."""
    entry_date = date.date()
    
    with console.status("[bold yellow]Updating learning entry...", spinner="line"):
        try:
            learning_entry = service.get_learnings(entry_date)
            
            if not learning_entry.learnings or id > len(learning_entry.learnings) or id <= 0:
                console.print(f"[bold red]❌ Error:[/] Invalid learning ID. Learning with ID {id} not found.")
                return
            
            # Get existing learning and update only provided fields
            learning = learning_entry.learnings[id-1]
            
            # Show current values
            console.print(f"[dim]Current topic: [/][italic]{learning.topic}[/]")
            console.print(f"[dim]Current insight: [/][italic]{learning.insight}[/]")
            if learning.connection:
                console.print(f"[dim]Current connection: [/][italic]{learning.connection}[/]")
            
            if topic:
                learning.topic = topic
            if insight:
                learning.insight = insight
            if connection is not None:  # Allow empty string to clear connection
                learning.connection = connection if connection else None
            
            # Save updated learning entry
            service.save_learnings(learning_entry, entry_date)
            
            console.print(f"[bold green]✅ Learning #{id} updated successfully![/]")
        except Exception as e:
            console.print(f"[bold red]❌ Error:[/] {str(e)}")

@learnings.command()
@click.option('--date', '-d', type=click.DateTime(formats=["%Y-%m-%d"]), 
              default=str(date.today()), help="Date to delete learning from (YYYY-MM-DD)")
@click.option('--id', '-i', type=int, prompt="🔍 Learning ID to delete", help="ID of the learning to delete")
@click.confirmation_option(prompt="❗ Are you sure you want to delete this learning?")
def delete(date: datetime, id: int):
    """🗑️ Delete a learning entry."""
    entry_date = date.date()
    
    with console.status("[bold red]Deleting learning entry...", spinner="point"):
        try:
            learning_entry = service.get_learnings(entry_date)
            
            if not learning_entry.learnings or id > len(learning_entry.learnings) or id <= 0:
                console.print(f"[bold red]❌ Error:[/] Invalid learning ID. Learning with ID {id} not found.")
                return
            
            # Show what's being deleted
            learning = learning_entry.learnings[id-1]
            console.print(f"[dim]Deleting topic: [/][italic]{learning.topic}[/]")
            
            # Remove learning
            del learning_entry.learnings[id-1]
            
            # Save updated learning entry
            service.save_learnings(learning_entry, entry_date)
            
            console.print(f"[bold green]✅ Learning #{id} deleted successfully![/]")
        except Exception as e:
            console.print(f"[bold red]❌ Error:[/] {str(e)}")