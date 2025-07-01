# engine/models.py

from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field

# Using Pydantic models ensures that the data loaded from YAML
# conforms to our expected structure. It provides automatic validation
# and clear error messages, which is crucial for an engine that
# needs to be robust to user-created story files.

# Forward references are used for models that refer to each other.
# Pydantic resolves these at a later stage.


class Condition(BaseModel):
    """
    A single condition that can be checked against the game state.
    A choice can have a list of these, and all must be true for
    the choice to be available.
    The structure uses a dictionary with a single key, making it
    extensible for new condition types.
    e.g., {"has_item": "key"} or {"stat_gte": ["strength", 10]}
    """
    has_item: Optional[str] = None
    lacks_item: Optional[str] = None
    flag_is: Optional[List[Union[str, bool]]] = None
    stat_equals: Optional[List[Union[str, int]]] = None
    stat_gte: Optional[List[Union[str, int]]] = None
    stat_lte: Optional[List[Union[str, int]]] = None

    def __repr__(self) -> str:
        # A more readable representation for debugging.
        condition_type, value = self.get_condition_parts()
        return f"<Condition: {condition_type} {value}>"

    def get_condition_parts(self):
        """Helper to unpack the condition for the evaluator."""
        for key, value in self.model_dump().items():
            if value is not None:
                return key, value
        return None, None


class Effect(BaseModel):
    """
    A single effect that can be applied to the game state.
    A choice can have a list of these that are applied when chosen.
    The structure is a single-key dictionary for extensibility.
    e.g., {"add_item": "sword"} or {"add_to_stat": ["gold", 50]}
    """
    add_item: Optional[str] = None
    remove_item: Optional[str] = None
    set_flag: Optional[List[Union[str, bool]]] = None
    set_stat: Optional[List[Union[str, int]]] = None
    add_to_stat: Optional[List[Union[str, int]]] = None

    def __repr__(self) -> str:
        effect_type, value = self.get_effect_parts()
        return f"<Effect: {effect_type} {value}>"

    def get_effect_parts(self):
        """Helper to unpack the effect for the state manager."""
        for key, value in self.model_dump().items():
            if value is not None:
                return key, value
        return None, None


class Choice(BaseModel):
    """Represents a single choice a player can make in a scene."""
    text: str
    next_scene_id: str = Field(..., alias="next_scene_id")
    conditions: Optional[List[Condition]] = Field(default_factory=list)
    effects: Optional[List[Effect]] = Field(default_factory=list)

    def __repr__(self) -> str:
        return f"<Choice: '{self.text}' -> {self.next_scene_id}>"


class Scene(BaseModel):
    """Represents a single scene or node in the adventure."""
    description: str
    choices: Optional[List[Choice]] = Field(default_factory=list)

    def is_terminal(self) -> bool:
        """A scene is terminal if it has no choices."""
        return not self.choices


class InitialState(BaseModel):
    """Defines the player's state at the start of the adventure."""
    stats: Dict[str, int] = Field(default_factory=dict)
    inventory: List[str] = Field(default_factory=list)
    flags: Dict[str, bool] = Field(default_factory=dict)


class Story(BaseModel):
    """The root model for an entire story file."""
    title: str
    author: str
    version: str
    start_scene_id: str = Field(..., alias="start_scene_id")
    initial_state: InitialState = Field(default_factory=InitialState)
    scenes: Dict[str, Scene]
