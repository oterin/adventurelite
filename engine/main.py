# engine/main.py

import sys

from . import loader
from .engine import GameEngine
from .renderer import Renderer
from .exceptions import AdventureLiteException


def main():
    """
    The main function for the AdventureLite game engine.
    """
    renderer = Renderer()
    try:
        # 1. Discover available stories
        stories = loader.discover_stories()
        if not stories:
            renderer.render_error(
                f"No stories found in the '{loader.STORIES_DIR}' directory.\n"
                "Please create a story to begin."
            )
            sys.exit(1)

        # 2. Prompt user to select a story
        story_name = renderer.render_story_list(list(stories.keys()))

        # 3. Load the selected story
        renderer.console.print(f"\nLoading '{story_name}'...")
        story = loader.load_story(story_name)

        # 4. Initialize and run the game engine
        engine = GameEngine(story, renderer)
        engine.run()

    except AdventureLiteException as e:
        # Handle our custom exceptions gracefully
        renderer.render_error(str(e))
        sys.exit(1)
    except (KeyboardInterrupt, EOFError):
        # Handle Ctrl+C or Ctrl+D
        renderer.console.print("\n\n[bold yellow]Exiting game. Goodbye![/bold yellow]")
        sys.exit(0)
    except Exception as e:
        # Catch-all for any other unexpected errors
        renderer.render_error(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()