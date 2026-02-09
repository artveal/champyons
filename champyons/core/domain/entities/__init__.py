"""
Domain Entities Module

This module contains all domain entities organized by context.

Submodules:
-----------
- geography: Geographic entities (Continent, Nation, City...)
- people: Person-related entities (Player, Staff...)
- teams: Team and club entities (Team, Stadium...)
- matches: Match simulation entities (Match, MatchEvent...)
- competitions: Competition entities (Competition, Season...)

Usage:
------
You can import entities from their specific submodules:

    from champyons.core.domain.entities.geography import Continent, Nation
    from champyons.core.domain.entities.people import Player
    from champyons.core.domain.entities.teams import Team
    from champyons.core.domain.entities.matches import Match
    from champyons.core.domain.entities.competitions import Competition

Or import entire submodules:

    from champyons.core.domain import entities
    
    # Access entities via submodules
    continent = entities.geography.Continent(...)
    player = entities.people.Player(...)

Architecture Notes:
-------------------
- Entities are rich domain objects with behavior and identity
- They encapsulate business rules and invariants
- They should be framework-agnostic (no SQLAlchemy, no Pydantic here)
- Persistence is handled by repositories (adapters layer)
- Entities can reference each other by ID to avoid tight coupling

Entity Design Principles:
-------------------------
1. **Identity**: Entities have a unique identifier (usually `id`)
2. **Mutability**: Entities can change state over time
3. **Business Logic**: Entities contain domain logic, not just data
4. **Validation**: Entities validate their own invariants
5. **Events**: Entities can raise domain events when state changes

Mixins:
-------
Common behaviors are extracted into mixins:
- ActiveMixin: Soft delete functionality. Disabled entities are considered inactive (e.g. retired people, extinct teams...)
- TimestampMixin: Created/updated timestamps
- GeographyMixin: include geonames id to enable Geonames syncronization
- AuthorMixin: Track who created/modified

See: champyons.core.domain.entities.mixins
"""

# Import submodules for easy access
from . import geography
from . import mixins
from . import people
from . import teams
from . import matches
from . import competitions

# Import the User entity (it's standalone)
from .user import User

# Convenience exports for common entities
# (Uncomment as entities are implemented)
from .geography import (
    Continent,
    Nation,
    Region,
    LocalRegion,
    City,
    Nationality
)

# from .people import Player, Person
# from .teams import Team, Squad
# from .matches import Match, MatchEvent
# from .competitions import Competition, Season

__all__ = [
    # Submodules
    "geography",
    "people",
    "teams", 
    "matches",
    "competitions",
    "mixins",
    
    # Standalone entities
    "User",
    
    # Geography entities
    "Continent",
    "Nation",
    "Region",
    "LocalRegion",
    "City",
    "Nationality"
    
    # People entities (uncomment when implemented)
    # "Player",
    # "Person",
    
    # Team entities (uncomment when implemented)
    # "Team",
    # "Squad",
    
    # Match entities (uncomment when implemented)
    # "Match",
    # "MatchEvent",
    
    # Competition entities (uncomment when implemented)
    # "Competition",
    # "Season",
]
