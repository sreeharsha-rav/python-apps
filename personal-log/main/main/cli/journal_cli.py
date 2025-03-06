import click
from datetime import date, datetime, timedelta
from typing import Dict, Any, Optional, List
import json
import os
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.layout import Layout
from rich.box import ROUNDED, SIMPLE, HEAVY
from rich.text import Text
from rich.rule import Rule
from rich.markdown import Markdown
from rich.columns import Columns
from rich.align import Align
from rich.style import Style
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import box

# # Try to import Calendar, but provide a fallback
# try:
#     from rich.calendar import Calendar
#     HAS_CALENDAR = True
# except ImportError:
#     HAS_CALENDAR = False

from main.storage.json_file_manager import JSONFileManager

console = Console()
file_manager = JSONFileManager("./data")

@click.group()
def journal():
    """View and manage your complete journal."""
    pass

@journal.command("view")
@click.option('--date', '-d', type=click.DateTime(formats=["%Y-%m-%d"]), 
              default=str(date.today()), help="Date to view journal (YYYY-MM-DD)")
@click.option('--pretty/--raw', default=False, help="Pretty format or raw JSON")      # displays raw by default
def view(date: datetime, pretty: bool):
    """View the complete journal for a specific date."""
    entry_date = date.date()
    
    # Construct the file path
    file_path = file_manager.storage_dir / file_manager.get_filename(entry_date)
    
    if not file_path.exists():
        console.print(f"[yellow]No journal entries found for {entry_date}[/]")
        return
    
    try:
        # Display a spinner while loading
        with Progress(
            SpinnerColumn(),
            TextColumn("[bold blue]Loading journal entry..."),
            transient=True,
        ) as progress:
            progress.add_task("Loading", total=None)
            # Load the JSON data
            with open(file_path, 'r') as f:
                data = json.load(f)
        
        if not pretty:
            # Display raw JSON with syntax highlighting
            console.print_json(json.dumps(data))
            return
        
        # TODO: # Display pretty formatted journal
        # console.print(Panel.fit(
        #     f"[bold]Personal Journal[/bold]",
        #     subtitle=f"{entry_date.strftime('%A, %B %d, %Y')}",
        #     style="blue",
        #     box=HEAVY
        # ))
        
        # # Create layout sections
        # layout = Layout()
        # layout.split_column(
        #     Layout(name="main")
        # )
        
        # # Split main into sections
        # layout["main"].split_column(
        #     Layout(name="intentions", ratio=4),
        #     Layout(name="thoughts", ratio=3),
        #     Layout(name="learnings", ratio=3),
        #     Layout(name="reflections", ratio=2),
        # )
        
        # # === INTENTIONS SECTION ===
        # if "daily_intentions" in data:
        #     intentions_data = data["daily_intentions"]
        #     intentions_panel = Panel(
        #         _format_intentions(intentions_data),
        #         title="[bold blue]Intentions & Priorities[/]",
        #         border_style="blue",
        #         box=box.ROUNDED,
        #         padding=(1, 2),
        #     )
        #     layout["intentions"].update(intentions_panel)
        # else:
        #     layout["intentions"].update(Panel("[italic]No intentions set for today[/]", 
        #                                  title="[bold blue]Intentions & Priorities[/]",
        #                                  border_style="blue"))
        
        # # === THOUGHTS SECTION ===
        # if "fleeting_thoughts" in data and data["fleeting_thoughts"].get("thoughts"):
        #     thoughts_data = data["fleeting_thoughts"]
        #     thoughts_panel = Panel(
        #         _format_thoughts(thoughts_data),
        #         title="[bold green]Fleeting Thoughts[/]",
        #         border_style="green",
        #         box=box.ROUNDED,
        #         padding=(1, 2),
        #     )
        #     layout["thoughts"].update(thoughts_panel)
        # else:
        #     layout["thoughts"].update(Panel("[italic]No thoughts recorded for today[/]", 
        #                               title="[bold green]Fleeting Thoughts[/]",
        #                               border_style="green"))
        
        # # === LEARNINGS SECTION ===
        # if "learnings" in data and data["learnings"].get("learnings"):
        #     learnings_data = data["learnings"]
        #     learnings_panel = Panel(
        #         _format_learnings(learnings_data),
        #         title="[bold magenta]Learnings[/]",
        #         border_style="magenta",
        #         box=box.ROUNDED,
        #         padding=(1, 2),
        #     )
        #     layout["learnings"].update(learnings_panel)
        # else:
        #     layout["learnings"].update(Panel("[italic]No learnings recorded for today[/]", 
        #                                title="[bold magenta]Learnings[/]",
        #                                border_style="magenta"))
        
        # # === REFLECTIONS SECTION ===
        # if "reflections" in data:
        #     reflections_data = data["reflections"]
        #     print(reflections_data)
        #     reflections_panel = Panel(
        #         _format_reflections(reflections_data),
        #         title="[bold yellow]Reflections[/]",
        #         border_style="yellow",
        #         box=box.ROUNDED,
        #         padding=(1, 2),
        #     )
        #     layout["reflections"].update(reflections_panel)
        # else:
        #     layout["reflections"].update(Panel("[italic]No reflections recorded for today[/]", 
        #                                  title="[bold yellow]Reflections[/]",
        #                                  border_style="yellow"))
        
        # # Print the layout
        # console.print(layout)
        
        # # Navigation footer
        # yesterday = entry_date - timedelta(days=1)
        # tomorrow = entry_date + timedelta(days=1)
        # yesterday_exists = file_manager.file_exists(yesterday)
        # tomorrow_exists = file_manager.file_exists(tomorrow)
        
        # nav_text = Text()
        # if yesterday_exists:
        #     nav_text.append(f"← Yesterday ({yesterday}) ", style="blue bold")
        # if yesterday_exists and tomorrow_exists:
        #     nav_text.append(" | ")
        # if tomorrow_exists:
        #     nav_text.append(f"Tomorrow ({tomorrow}) →", style="blue bold")
        
        # if nav_text:
        #     console.print()
        #     console.print(Align.center(Panel(nav_text, box=box.SIMPLE)))
        #     console.print(Align.center("[dim]Use -d option to navigate to a specific date[/]"))
        
    except Exception as e:
        console.print(f"[bold red]Error:[/] {str(e)}")

@journal.command("calendar")
@click.option('--month', '-m', type=int, default=datetime.now().month, help="Month (1-12)")
@click.option('--year', '-y', type=int, default=datetime.now().year, help="Year")
def calendar_view(month: int, year: int):
    """Display a calendar with entries marked."""
    try:
        all_dates = file_manager.get_all_dates()
        entries_this_month = [d for d in all_dates if d.month == month and d.year == year]
        
        # if not HAS_CALENDAR:
        # Fallback implementation without rich.calendar
        # console.print("[yellow]Rich Calendar module not available. Using simple table view instead.[/]")
        
        # Display a simple list of dates with entries
        table = Table(title=f"Journal Entries - {datetime(year, month, 1).strftime('%B %Y')}")
        table.add_column("Date", style="cyan")
        table.add_column("Day", style="green")
        
        for entry_date in sorted(entries_this_month):
            day_name = entry_date.strftime("%A")
            table.add_row(str(entry_date), day_name)
        
        console.print(table)
        console.print(f"[green]Found {len(entries_this_month)} entries for this month[/]")
        return
        
        # # Original code with rich.calendar
        # cal = Calendar(month=month, year=year, style="blue", 
        #               date_callback=lambda d: Style(bgcolor="green") if date(year, month, d) in entries_this_month else None)
        
        # console.print(Panel.fit(
        #     cal,
        #     title=f"[bold blue]Journal Entries - {datetime(year, month, 1).strftime('%B %Y')}[/]",
        #     border_style="blue",
        #     padding=(1, 2),
        # ))
        
        # # Display entry counts
        # console.print(f"[green]Found {len(entries_this_month)} entries for this month[/]")
        # console.print("[dim]Green dates have journal entries. Use 'view -d DATE' to view an entry.[/]")
        
    except Exception as e:
        console.print(f"[bold red]Error:[/] {str(e)}")

@journal.command("stats")
@click.option('--month', '-m', type=int, default=datetime.now().month, help="Month (1-12)")
@click.option('--year', '-y', type=int, default=datetime.now().year, help="Year")
def stats(month: int, year: int):
    """View statistics about your journal entries."""
    try:
        all_dates = file_manager.get_all_dates()
        entries_this_month = [d for d in all_dates if d.month == month and d.year == year]
        
        # Create a nice stats display
        stats_table = Table(title=f"Journal Stats for {datetime(year, month, 1).strftime('%B %Y')}")
        stats_table.add_column("Metric", style="cyan", justify="right")
        stats_table.add_column("Value", style="magenta")
        
        # Calculate stats
        total_entries = len(entries_this_month)
        days_in_month = (datetime(year, month + (1 if month < 12 else -11), 1) - 
                        datetime(year, month, 1)).days
        
        entry_streak = _calculate_streak(all_dates)
        
        stats_table.add_row("Total Entries", str(total_entries))
        stats_table.add_row("Days in Month", str(days_in_month))
        stats_table.add_row("Coverage", f"{(total_entries/days_in_month)*100:.1f}%")
        stats_table.add_row("Current Streak", f"{entry_streak} days")
        
        # Analyze entry contents
        thoughts_count = 0
        learnings_count = 0
        reflections_count = 0
        
        for entry_date in entries_this_month:
            data = file_manager.read_data(entry_date)
            if "fleeting_thoughts" in data and data["fleeting_thoughts"].get("thoughts"):
                thoughts_count += len(data["fleeting_thoughts"]["thoughts"])
            if "learnings" in data and data["learnings"].get("learnings"):
                learnings_count += len(data["learnings"]["learnings"])
            if "reflections" in data and data["reflections"].get("learning_reflections"):
                if data["reflections"]["learning_reflections"].get("keyTakeaways"):
                    reflections_count += len(data["reflections"]["learning_reflections"]["keyTakeaways"])
        
        stats_table.add_section()
        stats_table.add_row("Total Thoughts", str(thoughts_count))
        stats_table.add_row("Total Learnings", str(learnings_count))
        stats_table.add_row("Total Reflections", str(reflections_count))
        
        console.print(stats_table)
        
    except Exception as e:
        console.print(f"[bold red]Error:[/] {str(e)}")


def _calculate_streak(dates: List[date]) -> int:
    """Calculate the current streak of consecutive days with entries"""
    if not dates:
        return 0
        
    sorted_dates = sorted(dates, reverse=True)
    today = date.today()
    
    # Check if today has an entry
    if sorted_dates[0] != today:
        return 0
        
    streak = 1
    for i in range(1, len(sorted_dates)):
        if sorted_dates[i-1] - sorted_dates[i] == timedelta(days=1):
            streak += 1
        else:
            break
            
    return streak


# def _format_intentions(intentions_data: Dict[str, Any]) -> Text:
#     """Format intentions data for display"""
#     text = Text()
    
#     # Affirmation
#     if (intentions_data.get("intentions") and 
#         intentions_data["intentions"].get("affirmation")):
#         text.append("💭 [bold yellow]Affirmation:[/]\n")
#         text.append(f'   "{intentions_data["intentions"]["affirmation"]}"\n\n')
    
#     # Goals
#     if intentions_data.get("intentions"):
#         # Long term goals
#         if intentions_data["intentions"].get("long_term_goals"):
#             text.append("🌟 [bold]Long-term Goals:[/]\n")
#             for i, goal in enumerate(intentions_data["intentions"]["long_term_goals"], 1):
#                 text.append(f"   {i}. {goal}\n")
#             text.append("\n")
        
#         # Short term goals
#         if intentions_data["intentions"].get("short_term_goals"):
#             text.append("✨ [bold]Short-term Goals:[/]\n")
#             for i, goal in enumerate(intentions_data["intentions"]["short_term_goals"], 1):
#                 text.append(f"   {i}. {goal}\n")
#             text.append("\n")
    
#     # Priorities
#     if intentions_data.get("priorities"):
#         text.append("🎯 [bold]Today's Priorities:[/]\n")
#         for i, priority in enumerate(intentions_data["priorities"], 1):
#             text.append(f"   {i}. [bold]{priority['task']}[/]")
#             if priority.get("alignment"):
#                 text.append(f" - [italic]{priority['alignment']}[/]")
#             text.append("\n")
    
#     return text

# def _format_thoughts(thoughts_data: Dict[str, Any]) -> Text:
#     """Format thoughts data for display"""
#     text = Text()
    
#     if thoughts_data.get("thoughts"):
#         for i, thought in enumerate(thoughts_data["thoughts"], 1):
#             print("THOUGHT", thought)
#             time_str = thought["timestamp"].split("T")[1][:5]  # Extract HH:MM from timestamp
#             text.append(f"[dim][{time_str}][/] ")
#             text.append(f"{thought['content']}\n\n")
    
#     return text

# def _format_learnings(learnings_data: Dict[str, Any]) -> Text:
#     """Format learnings data for display"""
#     text = Text()
    
#     if learnings_data.get("learnings"):
#         for i, learning in enumerate(learnings_data["learnings"], 1):
#             text.append(f"📝 [bold]#{i}: {learning['topic']}[/]\n")
#             text.append(f"   {learning['insight']}\n")
#             if learning.get("connection"):
#                 text.append(f"   [italic]Connection: {learning['connection']}[/]\n")
#             text.append("\n")
    
#     return text

# def _format_reflections(reflections_data: Dict[str, Any]) -> Text:
#     """Format reflections data for display"""
#     text = Text()
    
#     if reflections_data.get("thoughts_reflections"):
#         text.append(f"[bold]General Reflections:[/]\n")
#         text.append(f"{reflections_data['thoughts_reflections']}\n\n")
    
#     if reflections_data.get("learning_reflections"):
#         lr = reflections_data["learning_reflections"]
        
#         if lr.get("keyTakeaways"):
#             text.append("[bold]Key Takeaways:[/]\n")
#             for i, takeaway in enumerate(lr["keyTakeaways"], 1):
#                 text.append(f"   {i}. {takeaway}\n")
#             text.append("\n")
            
#         if lr.get("actionItems"):
#             text.append("[bold]Action Items:[/]\n")
#             for i, action in enumerate(lr["actionItems"], 1):
#                 text.append(f"   {i}. {action}\n")
    
#     return text