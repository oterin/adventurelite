# engine/renderer.py

import sys
from typing import List

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt

from .models import Choice

# Using a dedicated renderer class encapsulates all the presentation logic.
# If we wanted to switch from 'rich' to another UI library, or even a GUI,
# we would only need to change this file.

class Renderer:
    """Handles all rendering to the terminal using the 'rich' library."""

    def __init__(self):
        self.console = Console()

    def clear_screen(self):
        """Clears the console screen."""
        self.console.clear()

    def render_story_list(self, stories: List[str]) -> str:
        """
        Displays the list of available stories and prompts the user to choose one.
        """
        self.clear_screen()
        self.console.print(Panel("[bold cyan]Welcome to AdventureLite![/bold cyan]",
                                 title="Main Menu", border_style="green"))
        self.console.print("\n[bold]Please choose a story to play:[/bold]\n")

        for i, story_name in enumerate(stories, 1):
            self.console.print(f"  [yellow]{i}[/yellow]. {story_name}")

        self.console.print()
        choice = Prompt.ask("[bold]Enter the number of your choice[/bold]",
                              choices=[str(i) for i in range(1, len(stories) + 1)])
        return stories[int(choice) - 1]

    def render_scene(self, scene_description: str, story_title: str) -> None:
        """
        Renders the main scene view, including the description and title.
        """
        self.clear_screen()
        panel_content = Markdown(scene_description, style="italic")
        self.console.print(Panel(panel_content, title=story_title, border_style="cyan", padding=(1, 2)))

    def prompt_for_choice(self, choices: List[Choice]) -> Choice:
        """
        Displays the available choices and prompts the player for a decision.
        """
        self.console.print("\n[bold]What do you do?[/bold]\n")
        for i, choice in enumerate(choices, 1):
            self.console.print(f"  [yellow]{i}[/yellow]. {choice.text}")

        self.console.print()
        # Rich's Prompt class handles input validation for us.
        selection = Prompt.ask(
            "[bold]Enter the number of your choice[/bold]",
            choices=[str(i) for i in range(1, len(choices) + 1)],
            show_choices=False
        )
        return choices[int(selection) - 1]

    def render_game_over(self, final_description: str) -> None:
        """Displays the game over screen."""
        self.console.print(Panel(f"[bold red]GAME OVER[/bold red]\n\n{final_description}",
                                 border_style="red", padding=1))

    def render_error(self, message: str) -> None:
        """Displays an error message in a distinct format."""
        self.console.print(Panel(f"[bold red]Error:[/bold red] {message}",
                                 title="Error", border_style="red"))