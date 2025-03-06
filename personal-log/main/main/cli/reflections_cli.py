import click
from datetime import date, datetime
from typing import Optional, List
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.markdown import Markdown
from rich.prompt import Prompt, Confirm

from main.modules.reflections.model import Reflection, LearningReflections
from main.modules.reflections.service import ReflectionsService
from main.storage.json_file_manager import JSONFileManager

console = Console()
file_manager = JSONFileManager("./data")
service = ReflectionsService(file_manager)

@click.group()
def reflections():
    """Manage your daily reflections."""
    pass

@reflections.command()
@click.option('--date', '-d', type=click.DateTime(formats=["%Y-%m-%d"]), 
              default=str(date.today()), help="Date for the reflection (YYYY-MM-DD)")
def view(date: datetime):
    """View reflections for a specific date."""
    entry_date = date.date()
    
    try:
        reflection = service.get_reflection(entry_date)
        
        if not reflection:
            console.print(f"[yellow]No reflections found for {entry_date}[/]")
            return
        
        console.print(f"[bold green]Reflections for {entry_date}[/]")
        
        if reflection.thoughts_reflections:
            console.print(Panel.fit(
                reflection.thoughts_reflections,
                title="General Reflections",
                border_style="blue"
            ))
        
        if reflection.learning_reflections:
            if reflection.learning_reflections.key_takeaways:
                console.print("\n[bold]Key Takeaways:[/]")
                for i, takeaway in enumerate(reflection.learning_reflections.key_takeaways, 1):
                    console.print(f"  {i}. [green]{takeaway}[/]")
            
            if reflection.learning_reflections.action_items:
                console.print("\n[bold]Action Items:[/]")
                for i, action in enumerate(reflection.learning_reflections.action_items, 1):
                    console.print(f"  {i}. [blue]{action}[/]")
    except Exception as e:
        console.print(f"[bold red]Error:[/] {str(e)}")

@reflections.command()
@click.option('--date', '-d', type=click.DateTime(formats=["%Y-%m-%d"]), 
              default=str(date.today()), help="Date for creating reflection (YYYY-MM-DD)")
def create(date: datetime):
    """Create a complete reflection through interactive prompts."""
    entry_date = date.date()
    
    console.print(f"[bold]Creating reflections for {entry_date}[/]")
    
    # Check if reflections already exist
    existing_reflection = service.get_reflection(entry_date)
    if existing_reflection:
        if not Confirm.ask("[yellow]Reflections already exist for this date. Do you want to overwrite?[/]"):
            console.print("[yellow]Operation cancelled.[/]")
            return

    # Prompt for thoughts reflection
    console.print("\n[bold blue]General Thoughts Reflection[/]")
    console.print("[dim]What are your general reflections on today? How did it go?[/]")
    thoughts_text = Prompt.ask("Thoughts", default="")
    
    # Prompt for key takeaways
    console.print("\n[bold green]Key Takeaways[/]")
    console.print("[dim]What did you learn today? Enter takeaways one by one (empty line to finish)[/]")
    key_takeaways = []
    while True:
        takeaway = Prompt.ask("Takeaway", default="")
        if not takeaway:
            break
        key_takeaways.append(takeaway)
    
    # Prompt for action items
    console.print("\n[bold cyan]Action Items[/]")
    console.print("[dim]What actions will you take based on today's experiences? (empty line to finish)[/]")
    action_items = []
    while True:
        action = Prompt.ask("Action", default="")
        if not action:
            break
        action_items.append(action)
    
    # Create and save the reflection
    try:
        learning_reflections = LearningReflections(
            key_takeaways=key_takeaways,
            action_items=action_items
        )
        
        reflection = Reflection(
            thoughts_reflections=thoughts_text if thoughts_text else None,
            learning_reflections=learning_reflections if (key_takeaways or action_items) else None
        )
        
        service.save_reflection(reflection, entry_date)
        
        console.print("\n[bold green]Reflection created successfully![/]")
        
        # Show a summary
        console.print("\n[bold]Reflection Summary:[/]")
        if thoughts_text:
            console.print(Panel(thoughts_text, title="General Reflections", border_style="blue", expand=False))
        
        if key_takeaways:
            console.print("\n[bold]Key Takeaways:[/]")
            for i, takeaway in enumerate(key_takeaways, 1):
                console.print(f"  {i}. [green]{takeaway}[/]")
        
        if action_items:
            console.print("\n[bold]Action Items:[/]")
            for i, action in enumerate(action_items, 1):
                console.print(f"  {i}. [blue]{action}[/]")
        
    except Exception as e:
        console.print(f"[bold red]Error:[/] {str(e)}")

@reflections.command()
@click.option('--date', '-d', type=click.DateTime(formats=["%Y-%m-%d"]), 
              default=str(date.today()), help="Date for the reflection (YYYY-MM-DD)")
@click.option('--text', '-t', prompt="Your reflection", help="Your thoughts reflection text")
def add_thoughts(date: datetime, text: str):
    """Add or update general thoughts reflection."""
    entry_date = date.date()
    
    try:
        service.update_thoughts_reflection(text, entry_date)
        console.print("[bold green]Thoughts reflection saved successfully![/]")
    except Exception as e:
        console.print(f"[bold red]Error:[/] {str(e)}")

@reflections.command()
@click.option('--date', '-d', type=click.DateTime(formats=["%Y-%m-%d"]), 
              default=str(date.today()), help="Date for the reflection (YYYY-MM-DD)")
@click.option('--takeaway', '-t', prompt="Key takeaway", help="Add a key takeaway")
def add_takeaway(date: datetime, takeaway: str):
    """Add a key takeaway to your learning reflections."""
    entry_date = date.date()
    
    try:
        service.add_key_takeaway(takeaway, entry_date)
        console.print("[bold green]Key takeaway added successfully![/]")
    except Exception as e:
        console.print(f"[bold red]Error:[/] {str(e)}")

@reflections.command()
@click.option('--date', '-d', type=click.DateTime(formats=["%Y-%m-%d"]), 
              default=str(date.today()), help="Date for the reflection (YYYY-MM-DD)")
@click.option('--action', '-a', prompt="Action item", help="Add an action item")
def add_action(date: datetime, action: str):
    """Add an action item to your learning reflections."""
    entry_date = date.date()
    
    try:
        service.add_action_item(action, entry_date)
        console.print("[bold green]Action item added successfully![/]")
    except Exception as e:
        console.print(f"[bold red]Error:[/] {str(e)}")

@reflections.command()
@click.option('--date', '-d', type=click.DateTime(formats=["%Y-%m-%d"]), 
              default=str(date.today()), help="Date for the reflection (YYYY-MM-DD)")
def clear(date: datetime):
    """Clear all reflections for a specific date."""
    entry_date = date.date()
    
    try:
        empty_reflection = Reflection()
        service.save_reflection(empty_reflection, entry_date)
        console.print(f"[bold green]Reflections for {entry_date} cleared successfully![/]")
    except Exception as e:
        console.print(f"[bold red]Error:[/] {str(e)}")