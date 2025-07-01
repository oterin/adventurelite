# engine/state.py

import copy
from typing import Dict, List, Any

from .models import InitialState, Condition, Effect
from .exceptions import GameStateException


class GameState:
    """
    Manages the player's state throughout the adventure.

    This class holds the player's stats, inventory, and flags, and
    provides methods to query and modify this state based on the
    rules defined in Condition and Effect objects. It also keeps
    track of the current scene.
    """

    def __init__(self, initial_state: InitialState, start_scene_id: str):
        # Deepcopy is important to ensure that if the game were to be
        # reset, the original initial_state object from the story model
        # remains unmodified.
        self.stats: Dict[str, int] = copy.deepcopy(initial_state.stats)
        self.inventory: List[str] = copy.deepcopy(initial_state.inventory)
        self.flags: Dict[str, bool] = copy.deepcopy(initial_state.flags)
        self.current_scene_id: str = start_scene_id

    def check_condition(self, condition: Condition) -> bool:
        """
        Evaluates a single condition against the current game state.

        Maps the condition type to a helper method that performs the
        actual check. This design is extensible: to add a new
        condition, one would add a new helper method and a new entry
        in the `condition_map`.
        """
        cond_type, value = condition.get_condition_parts()

        condition_map = {
            "has_item": self._check_has_item,
            "lacks_item": lambda v: not self._check_has_item(v),
            "flag_is": self._check_flag_is,
            "stat_equals": self._check_stat_equals,
            "stat_gte": self._check_stat_gte,
            "stat_lte": self._check_stat_lte,
        }

        if cond_type not in condition_map:
            raise GameStateException(f"Unknown condition type: {cond_type}")

        return condition_map[cond_type](value)

    def apply_effect(self, effect: Effect) -> None:
        """
        Applies a single effect, modifying the game state.

        Similar to `check_condition`, this maps effect types to
        helper methods, making it easy to extend with new effects.
        """
        effect_type, value = effect.get_effect_parts()

        effect_map = {
            "add_item": self._effect_add_item,
            "remove_item": self._effect_remove_item,
            "set_flag": self._effect_set_flag,
            "set_stat": self._effect_set_stat,
            "add_to_stat": self._effect_add_to_stat,
        }

        if effect_type not in effect_map:
            raise GameStateException(f"Unknown effect type: {effect_type}")

        effect_map[effect_type](value)

    # --- Condition Checker Methods ---

    def _check_has_item(self, item_name: str) -> bool:
        return item_name in self.inventory

    def _check_flag_is(self, flag_info: List[Any]) -> bool:
        flag_name, expected_value = flag_info
        return self.flags.get(flag_name, False) is expected_value

    def _check_stat_equals(self, stat_info: List[Any]) -> bool:
        stat_name, expected_value = stat_info
        return self.stats.get(stat_name, 0) == expected_value

    def _check_stat_gte(self, stat_info: List[Any]) -> bool:
        stat_name, value = stat_info
        return self.stats.get(stat_name, 0) >= value

    def _check_stat_lte(self, stat_info: List[Any]) -> bool:
        stat_name, value = stat_info
        return self.stats.get(stat_name, 0) <= value

    # --- Effect Applier Methods ---

    def _effect_add_item(self, item_name: str) -> None:
        if item_name not in self.inventory:
            self.inventory.append(item_name)

    def _effect_remove_item(self, item_name: str) -> None:
        if item_name in self.inventory:
            self.inventory.remove(item_name)

    def _effect_set_flag(self, flag_info: List[Any]) -> None:
        flag_name, value = flag_info
        self.flags[flag_name] = value

    def _effect_set_stat(self, stat_info: List[Any]) -> None:
        stat_name, value = stat_info
        self.stats[stat_name] = value

    def _effect_add_to_stat(self, stat_info: List[Any]) -> None:
        stat_name, value_to_add = stat_info
        self.stats[stat_name] = self.stats.get(stat_name, 0) + value_to_add