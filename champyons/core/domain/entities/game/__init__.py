"""
Geography Domain Entities

This module contains all geography-related domain entities used throughout
the Champyons football simulation game.

Notes:
------
- All entities inherit from mixins for common behavior (timestamps, active status, etc.)
- Geography entities form the foundation for player/team nationality
"""

from .game_state import GameState
from .season import Season

# Define what gets exported when using: from champyons.core.domain.entities.geography import *
__all__ = [
    "GameState",
    "Season",
]

# Type hints for IDE support (optional)
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    # This helps IDEs with type checking without circular imports
    from champyons.core.domain.entities.game.game_state import GameState as _GameState
    from champyons.core.domain.entities.game.season import Season as _Season