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
    stat_eq