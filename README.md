# AdventureLite Story Creation Guide

Welcome to the guide for creating stories for the AdventureLite engine! This document will walk you through the process of crafting your own interactive adventures using our simple yet powerful YAML-based format.

## 1. Project Structure

Each story must be contained within its own directory inside the `stories/` folder. The engine will recognize any directory here as a potential story.

Inside your story's directory, the main file must be named `story.yml`.

stories/
└── your_awesome_story/
└── story.yml


## 2. The `story.yml` File Format

The `story.yml` file is the heart of your adventure. It's written in YAML, a human-readable data format. It contains metadata about your story, the initial state of the player, and all the scenes that make up the narrative.

Here is the top-level structure:

```yaml
title: "Your Story Title"
author: "Your Name"
version: "1.0.0"
start_scene_id: "scene_01" # The ID of the very first scene
initial_state:
  # ... player's starting state
scenes:
  # ... a list of all scenes in your story
```

### 2.1. Metadata

*   `title` (required): The title of your adventure.
*   `author` (required): Your name.
*   `version` (required): The version of your story.
*   `start_scene_id` (required): The unique identifier for the scene where the player will begin.

### 2.2. Initial State (`initial_state`)

This section defines the player's state at the beginning of the game. It has three parts: `stats`, `inventory`, and `flags`. All are optional.

```yaml
initial_state:
  stats:
    health: 100
    mana: 50
    strength: 10
  inventory:
    - "rusty sword"
    - "healing potion"
  flags:
    knows_magic: false
    met_the_king: false
```

*   `stats`: A dictionary of numerical values that can increase or decrease.
*   `inventory`: A list of item names (strings) the player is carrying.
*   `flags`: A dictionary of boolean values (true/false) used to track events or conditions.

### 2.3. Scenes

The `scenes` section is a dictionary where each key is a unique `scene_id` and the value is a scene object.

```yaml
scenes:
  scene_01:
    # ... scene details ...
  scene_02:
    # ... scene details ...
```

Each scene object has the following structure:

*   `description` (required): The text that will be displayed to the player when they enter the scene. You can use basic markdown like `**bold**` or `*italic*`.
*   `choices` (optional): A list of choices the player can make. If a scene has no choices, it is an ending.

```yaml
scenes:
  scene_01:
    description: |
      You stand at a crossroads. A path leads **left** into a dark forest,
      and a path leads **right** towards a bustling town.
    choices:
      # ... list of choices ...
```

### 2.4. Choices

Choices are the heart of the interaction. Each choice in the `choices` list is an object with the following keys:

*   `text` (required): The text describing the choice.
*   `next_scene_id` (required): The `id` of the scene the player will go to if they pick this option.
*   `conditions` (optional): Rules that determine if this choice is visible.
*   `effects` (optional): Changes to the player's state that occur when this choice is made.

```yaml
choices:
  - text: "Go left into the forest."
    next_scene_id: "forest_entrance"
    effects:
      - set_flag: ["entered_forest", true]

  - text: "Use the silver key."
    next_scene_id: "unlocked_door"
    conditions:
      - has_item: "silver key"
```

## 3. Conditions and Effects (Advanced)

This is where the magic happens. You can make the story dynamic and reactive to the player's actions.

### 3.1. Conditions

Conditions are checked before a choice is displayed. If all conditions for a choice are met, it will be shown to the player. A condition is a dictionary with a single key representing the type of check.

Available conditions:
*   `has_item: "item_name"`: Checks if the player has `item_name` in their inventory.
*   `lacks_item: "item_name"`: Checks if the player does *not* have `item_name`.
*   `flag_is: ["flag_name", true]`: Checks if `flag_name` is set to `true` or `false`.
*   `stat_equals: ["stat_name", value]`: Checks if a stat is exactly `value`.
*   `stat_gte: ["stat_name", value]`: Checks if a stat is greater than or equal to `value`.
*   `stat_lte: ["stat_name", value]`: Checks if a stat is less than or equal to `value`.

Example: A choice that requires a key and for a flag to be true.
```yaml
conditions:
  - has_item: "silver key"
  - flag_is: ["met_the_king", true]
```

### 3.2. Effects

Effects are applied to the player's state *after* they make a choice, but *before* moving to the next scene. An effect is a dictionary with a single key representing the type of action.

Available effects:
*   `add_item: "item_name"`: Adds an item to the inventory.
*   `remove_item: "item_name"`: Removes an item from the inventory.
*   `set_flag: ["flag_name", true]`: Sets a flag to `true` or `false`.
*   `set_stat: ["stat_name", value]`: Sets a stat to a specific `value`.
*   `add_to_stat: ["stat_name", value]`: Adds `value` to a stat (can be negative).

Example: A choice that gives the player a sword and some gold.
```yaml
effects:
  - add_item: "iron sword"
  - add_to_stat: ["gold", 50]
  - set_flag: ["has_weapon", true]
```

That's it! With these tools, you can create complex, branching narratives. Happy writing!
