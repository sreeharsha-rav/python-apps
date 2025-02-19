from typing import Any, Dict
import random
from rich.console import Console
from rich.prompt import Prompt

console = Console()


class PromptManager:
    def __init__(self, prompts_data: Dict[str, Any]):
        self.prompts = prompts_data
        self.console = Console()

    def get_reflection_input(self, section: str) -> Dict[str, str]:
        """Get user input for opening or closing reflection."""
        prompts = self.prompts[section]["prompts"]
        selected_prompt = random.choice(prompts)

        console.print(f"\n[bold blue]{selected_prompt}[/bold blue]")
        response = Prompt.ask("Your response")

        return {"prompt": selected_prompt, "response": response}

    def get_module_input(self, module_name: str) -> Dict[str, str]:
        """Get user input for a specific module."""
        module_prompts = self.prompts["modules"][module_name]
        responses = {}

        console.print(
            f"\n[bold green]===== {module_name.replace('_', ' ').title()} ====="
        )

        for field, prompt_list in module_prompts.items():
            prompt = random.choice(prompt_list)
            console.print(f"\n[bold yellow]{prompt}[/bold yellow]")
            responses[field] = Prompt.ask("Your response")

        return responses
