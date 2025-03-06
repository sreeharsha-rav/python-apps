import click
from rich.console import Console
from rich.panel import Panel

# Import CLI modules
from main.cli.thoughts_cli import thoughts
from main.cli.reflections_cli import reflections
from main.cli.intentions_cli import intentions
from main.cli.learnings_cli import learnings
from main.cli.journal_cli import journal  # Import the new journal command

console = Console()

@click.group()
@click.version_option(version="1.0.0")
def cli():
    """Personal Log - Track your thoughts, activities, and reflections."""
    pass

# Add CLI modules as subcommands
cli.add_command(thoughts)
cli.add_command(reflections)
cli.add_command(intentions) 
cli.add_command(learnings)
cli.add_command(journal)  # Add the journal command

@cli.command()
def info():
    """Display information about Personal Log."""
    console.print(Panel.fit(
        "[bold]Personal Log[/]\n\n"
        "A CLI application for journaling, tracking thoughts, reflections, and learnings.\n\n"
        "[italic]Usage examples:[/]\n"
        "  - Add a thought: [blue]poetry run personal_log thoughts add[/]\n"
        "  - List today's reflections: [blue]poetry run personal_log reflections list[/]\n"
        "  - Set daily intentions: [blue]poetry run personal_log intentions set[/]\n"
        "  - Add a learning: [blue]poetry run personal_log learnings add[/]\n"
        "  - View full journal: [blue]poetry run personal_log journal[/]",
        title="About",
        border_style="green"
    ))

if __name__ == "__main__":
    cli()