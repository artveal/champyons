"""
Geography Domain Entities

This module contains all geography-related domain entities used throughout
the Champyons football simulation game.

Notes:
------
- All entities inherit from mixins for common behavior (timestamps, active status, etc.)
- Geography entities form the foundation for player/team nationality
"""

from .continent import Continent
from .country import Country
from .region import Region
from .local_region import LocalRegion
from .city import City
from .nationality import Nationality

# Define what gets exported when using: from champyons.core.domain.entities.geography import *
__all__ = [
    "Continent",
    "Country",
    "Region",
    "LocalRegion",
    "City",
    "Nationality"
]

# Type hints for IDE support (optional)
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    # This helps IDEs with type checking without circular imports
    from champyons.core.domain.entities.geography.continent import Continent as _Continent
    from champyons.core.domain.entities.geography.country import Country as _Country
    from champyons.core.domain.entities.geography.region import Region as _Region
    from champyons.core.domain.entities.geography.local_region import LocalRegion as _LocalRegion
    from champyons.core.domain.entities.geography.city import City as _City
    from champyons.core.domain.entities.geography.nationality import Nationality as _Nationality