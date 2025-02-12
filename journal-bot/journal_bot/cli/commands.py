import click
from rich.console import Console
from journal_bot.core.journal_entry import JournalEntry
from journal_bot.cli.prompts import PromptManager
from journal_bot.storage.json_storage import JsonStorage
from journal_bot.utils.config import load_prompts

console = Console()

@click.group()
def cli():
    """Journal Bot - Your personal journaling companion"""
    pass

@cli.command()
def new():
    """Create a new journal entry"""
    prompts = load_prompts()
    prompt_manager = PromptManager(prompts)
    storage = JsonStorage()

    # Get opening reflection
    opening = prompt_manager.get_reflection_input("opening_reflection")

    # Get mandatory modules
    modules = {
        "emotional_awareness": prompt_manager.get_module_input("emotional_awareness"),
        "growth_reflection": prompt_manager.get_module_input("growth_reflection")
    }

    # Optional modules
    if click.confirm("Would you like to reflect on gratitude and joy?"):
        modules["gratitude_joy"] = prompt_manager.get_module_input("gratitude_joy")
    
    if click.confirm("Would you like to focus on future possibilities?"):
        modules["future_focused"] = prompt_manager.get_module_input("future_focused")

    # Get closing reflection
    closing = prompt_manager.get_reflection_input("closing_integration")

    # Create and save entry
    entry = JournalEntry(
        opening_reflection=opening,
        modules=modules,
        closing_integration=closing
    )
    
    storage.save_entry(entry)
    console.print("[green]Journal entry saved successfully![/green]")

@cli.command()
def list():
    """List all journal entries"""
    storage = JsonStorage()
    entries = storage.list_entries()
    # Implementation for listing entries
