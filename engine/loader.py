# engine/loader.py

import os
from pathlib import Path
from typing import List, Dict

import yaml
from pydantic import ValidationError

from .models import Story
from .exceptions import StoryLoadException, StoryNotFoundException

STORIES_DIR = "stories"


def discover_stories() -> Dict[str, Path]:
    """
    Finds all valid stories in the stories directory.

    A valid story is a subdirectory of STORIES_DIR that contains
    a 'story.yml' file.

    Returns:
        A dictionary mapping the story name (directory name) to its
        story.yml file path.
    """
    base_path = Path(STORIES_DIR)
    if not base_path.is_dir():
        return {}

    story_paths = {}
    for entry in base_path.iterdir():
        if entry.is_dir():
            story_file = entry / "story.yml"
            if story_file.is_file():
                story_paths[entry.name] = story_file
    return story_paths


def load_story(story_name: str) -> Story:
    """
    Loads a story from a YAML file into a Pydantic model.

    Args:
        story_name: The name of the story (its directory name).

    Returns:
        A validated Story object.

    Raises:
        StoryNotFoundException: If the story directory doesn't exist.
        StoryLoadException: If the YAML is malformed or fails
                            pydantic validation.
    """
    story_paths = discover_stories()
    if story_name not in story_paths:
        raise StoryNotFoundException(f"Story '{story_name}' not found.")

    story_path = story_paths[story_name]

    try:
        with open(story_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            if not data:
                raise StoryLoadException("Story file is empty.")
    except yaml.YAMLError as e:
        raise StoryLoadException(f"Error parsing YAML in {story_path}: {e}") from e

    try:
        story = Story.model_validate(data)
        return story
    except ValidationError as e:
        # Pydantic's error messages are very informative. We wrap them
        # in our custom exception to provide context.
        error_details = "\n".join([
            f"  - {err['loc']}: {err['msg']}" for err in e.errors()
        ])
        raise StoryLoadException(
            f"Story file '{story_path.name}' has validation errors:\n{error_details}"
        ) from e