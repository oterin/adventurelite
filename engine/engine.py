# engine/engine.py

from .models import Story, Choice
from .state import GameState
from .renderer import Renderer
from .exceptions import GameStateException

class GameEngine:
    """
    The main orchestrator for the adventure game.

    This class manages the game loop, coordinating between the story data,
    the player's state, and the renderer to create the interactive experience.
    """

    def __init__(self, story: Story, renderer: Renderer):
        self.story = story
        self.renderer = renderer
        # The game state is initialized from the story's starting conditions.
        self.game_state = GameState(
            initial_state=story.initial_state,
            start_scene_id=story.start_scene_id
        )

    def run(self) -> None:
        """Starts and runs the main game loop."""
        while True:
            try:
                current_scene = self.story.scenes.get(self.game_state.current_scene_id)
                if not current_scene:
                    raise GameStateException(
                        f"FATAL: Scene '{self.game_state.current_scene_id}' not found in story."
                    )

                self.renderer.render_scene(current_scene.description, self.story.title)

                if current_scene.is_terminal():
                    self.renderer.render_game_over(current_scene.description)
                    break

                available_choices = self._get_available_choices(current_scene.choices)

                # A "soft lock" state where the player has no valid actions.
                if not available_choices:
                    self.renderer.render_game_over("You are stuck and can't find a way to proceed. Your adventure ends here.")
                    break

                chosen_choice = self.renderer.prompt_for_choice(available_choices)
                self._process_choice(chosen_choice)

            except GameStateException as e:
                self.renderer.render_error(str(e))
                break # Exit gracefully on internal errors

    def _get_available_choices(self, choices: list[Choice]) -> list[Choice]:
        """
        Filters the list of choices based on the current game state.
        A choice is available if all of its conditions are met.
        """
        available = []
        for choice in choices:
            if all(self.game_state.check_condition(cond) for cond in choice.conditions):
                available.append(choice)
        return available

    def _process_choice(self, choice: Choice) -> None:
        """
        Applies the effects of a chosen choice and updates the current scene.
        """
        # Apply all effects associated with the choice
        for effect in choice.effects:
            self.game_state.apply_effect(effect)

        # Transition to the next scene
        self.game_state.current_scene_id = choice.next_scene_id