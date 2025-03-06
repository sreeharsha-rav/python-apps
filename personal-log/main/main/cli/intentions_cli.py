import click
from datetime import date, datetime
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt

from main.modules.intentions.model import DailyIntentions, Intentions, Priority
from main.modules.intentions.service import IntentionsService
from main.storage.json_file_manager import JSONFileManager

console = Console()
file_manager = JSONFileManager("./data")
service = IntentionsService(file_manager)

@click.group()
def intentions():
    """Manage your daily intentions and priorities."""
    pass

@intentions.command()
@click.option('--date', '-d', type=click.DateTime(formats=["%Y-%m-%d"]), 
              default=str(date.today()), help="Date for intentions (YYYY-MM-DD)")
def show(date: datetime):
    """View intentions and priorities for a specific date."""
    entry_date = date.date()
    
    try:
        daily_intentions = service.get_daily_intentions(entry_date)
        
        if not daily_intentions:
            console.print(f"[yellow]No intentions found for {entry_date}[/]")
            return
        
        # Display intentions
        console.print(f"[bold green]Intentions for {entry_date}[/]\n")
        
        # Long-term goals
        if daily_intentions.intentions.long_term_goals:
            console.print("[bold]Long-term Goals:[/]")
            for i, goal in enumerate(daily_intentions.intentions.long_term_goals, 1):
                console.print(f"  {i}. [blue]{goal}[/]")
        
        # Short-term goals
        if daily_intentions.intentions.short_term_goals:
            console.print("\n[bold]Short-term Goals:[/]")
            for i, goal in enumerate(daily_intentions.intentions.short_term_goals, 1):
                console.print(f"  {i}. [cyan]{goal}[/]")
        
        # Affirmation
        if daily_intentions.intentions.affirmation:
            console.print("\n[bold]Affirmation:[/]")
            console.print(f"  [green italic]\"{daily_intentions.intentions.affirmation}\"[/]")
        
        # Priorities
        if daily_intentions.priorities:
            console.print("\n[bold]Priorities:[/]")
            table = Table(show_header=True, header_style="bold")
            table.add_column("#", style="dim", width=3)
            table.add_column("Task", style="green")
            table.add_column("Alignment", style="blue")
            
            for i, priority in enumerate(daily_intentions.priorities, 1):
                table.add_row(str(i), priority.task, priority.alignment)
            
            console.print(table)
    except Exception as e:
        console.print(f"[bold red]Error:[/] {str(e)}")

@intentions.command()
@click.option('--date', '-d', type=click.DateTime(formats=["%Y-%m-%d"]), 
              default=str(date.today()), help="Date for intentions (YYYY-MM-DD)")
def set(date: datetime):
    """Set intentions and priorities interactively."""
    entry_date = date.date()
    
    console.print(f"[bold]Setting intentions for {entry_date}[/]")
    
    # Long-term goals
    console.print("\n[bold]Enter your long-term goals (empty line to finish):[/]")
    long_term_goals = []
    while True:
        goal = Prompt.ask("[blue]Long-term goal[/]", default="")
        if not goal:
            break
        long_term_goals.append(goal)
    
    # Short-term goals
    console.print("\n[bold]Enter your short-term goals (empty line to finish):[/]")
    short_term_goals = []
    while True:
        goal = Prompt.ask("[cyan]Short-term goal[/]", default="")
        if not goal:
            break
        short_term_goals.append(goal)
    
    # Affirmation
    affirmation = Prompt.ask("\n[green]Daily affirmation[/]", default="")
    
    # Priorities
    console.print("\n[bold]Enter your top 3 priorities for today:[/]")
    priorities = []
    for i in range(1, 4):
        task = Prompt.ask(f"[yellow]Priority {i} task[/]", default="")
        if not task:
            break
        alignment = Prompt.ask(f"[blue]How does this align with your goals?[/]", default="")
        priorities.append(Priority(task=task, alignment=alignment))
    
    # Create and save intentions
    intentions_obj = Intentions(
        long_term_goals=long_term_goals,
        short_term_goals=short_term_goals,
        affirmation=affirmation if affirmation else None
    )
    
    daily_intentions = DailyIntentions(
        intentions=intentions_obj,
        priorities=priorities
    )
    
    try:
        service.save_daily_intentions(daily_intentions, entry_date)
        console.print("[bold green]Intentions set successfully![/]")
    except Exception as e:
        console.print(f"[bold red]Error:[/] {str(e)}")

@intentions.command()
@click.option('--date', '-d', type=click.DateTime(formats=["%Y-%m-%d"]), 
              default=str(date.today()), help="Date to update affirmation (YYYY-MM-DD)")
@click.option('--text', '-t', prompt="Your affirmation", help="Your daily affirmation")
def set_affirmation(date: datetime, text: str):
    """Update just the daily affirmation."""
    entry_date = date.date()
    
    try:
        service.update_affirmation(text, entry_date)
        console.print(f"[bold green]Affirmation updated successfully![/]")
    except Exception as e:
        console.print(f"[bold red]Error:[/] Could not update affirmation: {str(e)}")