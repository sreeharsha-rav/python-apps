import click
from datetime import date, datetime
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich import box
from rich.columns import Columns
from rich.layout import Layout
from rich.style import Style
from rich.text import Text

from main.modules.intentions.model import DailyIntentions, Intentions, Priority
from main.modules.intentions.service import IntentionsService
from main.storage.json_file_manager import JSONFileManager

console = Console()
file_manager = JSONFileManager("./data")
service = IntentionsService(file_manager)

def print_header(text: str):
    """Print a stylized header."""
    console.print(f"\n[bold yellow]{'-'*50}[/]")
    console.print(f"[bold cyan]{text.center(50)}[/]")
    console.print(f"[bold yellow]{'-'*50}[/]\n")

@click.group()
def intentions():
    """🎯 Set and manage your daily intentions and priorities ✨"""
    pass

@intentions.command()
@click.option('--date', '-d', type=click.DateTime(formats=["%Y-%m-%d"]), 
              default=str(date.today()), help="Date for intentions (YYYY-MM-DD)")
def show(date: datetime):
    """👁️ View your daily intentions and priorities 📋"""
    entry_date = date.date()
    
    with console.status(f"[bold blue]🔍 Loading intentions for {entry_date}...", spinner="dots"):
        try:
            daily_intentions = service.get_daily_intentions(entry_date)
            
            if not daily_intentions:
                console.print(Panel(
                    f"[yellow]No intentions found for {entry_date}[/]",
                    title="📭 Empty",
                    border_style="yellow"
                ))
                return
            
            print_header(f"✨ Intentions for {entry_date} ✨")
            
            # Create panels for goals
            panels = []
            
            # Long-term goals
            if daily_intentions.intentions.long_term_goals:
                long_term_content = "\n".join([f"📌 [blue]{goal}[/]" for goal in daily_intentions.intentions.long_term_goals])
                panels.append(Panel(long_term_content, title="🌟 Long-term Goals", border_style="blue", box=box.HEAVY))
            
            # Short-term goals
            if daily_intentions.intentions.short_term_goals:
                short_term_content = "\n".join([f"✅ [cyan]{goal}[/]" for goal in daily_intentions.intentions.short_term_goals])
                panels.append(Panel(short_term_content, title="🚀 Short-term Goals", border_style="cyan", box=box.HEAVY))
            
            # Display goals in columns
            if panels:
                console.print(Columns(panels))
            
            # Affirmation
            if daily_intentions.intentions.affirmation:
                console.print(Panel(
                    f"[green italic]\"{daily_intentions.intentions.affirmation}\"[/]",
                    title="💫 Daily Affirmation",
                    border_style="green",
                    box=box.DOUBLE_EDGE
                ))
            
            # Priorities
            if daily_intentions.priorities:
                console.print("\n[bold]📋 Today's Top Priorities:[/]")
                table = Table(show_header=True, header_style="bold magenta", box=box.HEAVY, border_style="bright_blue")
                table.add_column("№", style="dim", width=3)
                table.add_column("🎯 Priority", style="green")
                table.add_column("🔄 Goal Alignment", style="blue")
                
                for i, priority in enumerate(daily_intentions.priorities, 1):
                    table.add_row(
                        f"[bold]{i}[/]",
                        f"[green]{priority.task}[/]",
                        f"[blue italic]{priority.alignment}[/]"
                    )
                
                console.print(table)
                
        except Exception as e:
            console.print(Panel(
                f"[red]{str(e)}[/]",
                title="❌ Error",
                border_style="red"
            ))

@intentions.command()
@click.option('--date', '-d', type=click.DateTime(formats=["%Y-%m-%d"]), 
              default=str(date.today()), help="Date for intentions (YYYY-MM-DD)")
def set(date: datetime):
    """✍️ Set your daily intentions and priorities interactively"""
    entry_date = date.date()
    
    print_header(f"✨ Setting Intentions for {entry_date} ✨")
    
    # Long-term goals
    console.print(Panel("[bold]Enter your long-term goals[/] (press Enter with empty input to finish)", 
                       title="🌟 Long-term Goals", border_style="blue"))
    long_term_goals = []
    while True:
        goal = Prompt.ask("[blue]📌 Goal[/]", default="")
        if not goal:
            break
        long_term_goals.append(goal)
    
    # Short-term goals
    console.print(Panel("[bold]Enter your short-term goals[/] (press Enter with empty input to finish)", 
                       title="🚀 Short-term Goals", border_style="cyan"))
    short_term_goals = []
    while True:
        goal = Prompt.ask("[cyan]✅ Goal[/]", default="")
        if not goal:
            break
        short_term_goals.append(goal)
    
    # Affirmation
    console.print(Panel("[bold]What's your power statement for today?[/]", 
                       title="💫 Daily Affirmation", border_style="green"))
    affirmation = Prompt.ask("[green]✨ Affirmation[/]", default="")
    
    # Priorities
    console.print(Panel("[bold]What are your top 3 priorities for today?[/]", 
                       title="📋 Daily Priorities", border_style="magenta"))
    priorities = []
    for i in range(1, 4):
        task = Prompt.ask(f"[yellow]🎯 Priority {i}[/]", default="")
        if not task:
            break
        alignment = Prompt.ask(f"[blue]🔄 Goal alignment[/]", default="")
        priorities.append(Priority(task=task, alignment=alignment))
    
    # Save intentions
    try:
        intentions_obj = Intentions(
            long_term_goals=long_term_goals,
            short_term_goals=short_term_goals,
            affirmation=affirmation if affirmation else None
        )
        
        daily_intentions = DailyIntentions(
            intentions=intentions_obj,
            priorities=priorities
        )
        
        service.save_daily_intentions(daily_intentions, entry_date)
        console.print(Panel("✅ Intentions set successfully!", border_style="green"))
    except Exception as e:
        console.print(Panel(f"[red]{str(e)}[/]", title="❌ Error", border_style="red"))

# ... (keep existing set_affirmation command)