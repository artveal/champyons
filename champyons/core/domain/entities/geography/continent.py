from champyons.core.domain.entities.mixins.active import ActiveMixin
from champyons.core.domain.entities.mixins.geography import GeographyMixin
from champyons.core.domain.entities.mixins.timestamp import TimestampMixin

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from .country import Country

@dataclass
class Continent(ActiveMixin, GeographyMixin, TimestampMixin):
    ''' Represents a continental landmass (e.g., Europe, South America) '''
    id: Optional[int] = None
    code: str = ""
    name: str = ""

    # Relationships
    countries: List["Country"] = field(default_factory=list)