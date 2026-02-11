from champyons.core.domain.entities.mixins.active import ActiveMixin
from champyons.core.domain.entities.mixins.geography import GeographyMixin
from champyons.core.domain.entities.mixins.timestamp import TimestampMixin

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from .country import Country
    from .nationality import Nationality

@dataclass
class Continent(ActiveMixin, GeographyMixin, TimestampMixin):
    ''' Represents a continental landmass (e.g., Europe, South America) '''
    id: Optional[int] = None
    code: str = field(default="")
    name: str = field(default="")

    # Relationships
    countries: List["Country"] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.code or not self.code.strip():
            raise ValueError(f"Continent code cannot be empty")
        if not self.name or not self.name.strip():
            raise ValueError("Continent name cannot be empty") 